import gymnasium as gym
import numpy as np
import rospy
from gymnasium import spaces
from geometry_msgs.msg import PoseStamped, TwistStamped
from mavros_msgs.srv import CommandBool, SetMode
from mavros_msgs.msg import State
from gazebo_msgs.srv import SetModelState
from gazebo_msgs.msg import ModelState

class HoverEnv(gym.Env):
    def __init__(self):
        super(HoverEnv, self).__init__()
        # 动作空间：控制线速度 x, y, z
        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(3,), dtype=np.float32)
        # 观测空间：当前相对位置 x, y, z
        self.observation_space = spaces.Box(low=-10.0, high=10.0, shape=(3,), dtype=np.float32)

        rospy.init_node('rl_hover_env', anonymous=True)

        self.current_position = np.array([0.0, 0.0, 0.0])
        self.target_pos = np.array([0.0, 0.0, 2.0])
        self.current_state = State()
        self.control_mode = "POSITION" 
        self.current_action = np.array([0.0, 0.0, 0.0])

        # --- 订阅与发布 ---
        self.state_sub = rospy.Subscriber("/mavros/state", State, self.state_callback)
        self.pos_sub = rospy.Subscriber("/mavros/local_position/pose", PoseStamped, self.pose_callback)
        self.pos_pub = rospy.Publisher("/mavros/setpoint_position/local", PoseStamped, queue_size=10)
        self.vel_pub = rospy.Publisher("/mavros/setpoint_velocity/cmd_vel", TwistStamped, queue_size=10)

        # --- 服务 ---
        rospy.wait_for_service('/mavros/cmd/arming')
        self.arm_service = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool)
        self.mode_service = rospy.ServiceProxy('/mavros/set_mode', SetMode)
        self.set_state_proxy = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)

        # 启动 20Hz 后台控制线程
        self.timer = rospy.Timer(rospy.Duration(0.05), self.offboard_heartbeat)

    def state_callback(self, msg):
        self.current_state = msg

    def pose_callback(self, msg):
        self.current_position = np.array([msg.pose.position.x, msg.pose.position.y, msg.pose.position.z])

    def offboard_heartbeat(self, event):
        """核心：根据模式切换发布位置或速度"""
        try:
            if self.control_mode == "POSITION":
                msg = PoseStamped()
                msg.header.stamp = rospy.Time.now()
                msg.pose.position.x, msg.pose.position.y, msg.pose.position.z = 0, 0, 2.0
                self.pos_pub.publish(msg)
            else:
                msg = TwistStamped()
                msg.header.stamp = rospy.Time.now()
                msg.twist.linear.x, msg.twist.linear.y, msg.twist.linear.z = self.current_action
                self.vel_pub.publish(msg)
        except: pass

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        print("\n🔄 环境重置：执行物理纠偏与定点起飞...")

        # 1. 物理重置：对准模型名 iris，强制瞬移并清空速度惯性
        stop_msg = ModelState()
        stop_msg.model_name = 'iris' #
        stop_msg.pose.position.z = 0.15
        stop_msg.pose.orientation.w = 1.0
        try: self.set_state_proxy(stop_msg)
        except: pass
        rospy.sleep(0.5)

        # 2. 检查连接
        while not rospy.is_shutdown() and not self.current_state.connected:
            rospy.sleep(0.1)

        # 3. 辅助起飞：切换模式并解锁，死等高度稳定
        self.control_mode = "POSITION"
        stable_count = 0
        rate = rospy.Rate(10)
        print("🚀 正在辅助爬升至 2m 目标点...")

        while not rospy.is_shutdown():
            if self.current_state.mode != "OFFBOARD":
                self.mode_service(custom_mode='OFFBOARD')
            if not self.current_state.armed:
                self.arm_service(True)

            # 判定标准：高度在 1.9m~2.1m 之间且持续 1 秒才交权
            if 1.85 < self.current_position[2] < 2.15:
                stable_count += 1
            else:
                stable_count = 0

            if stable_count > 10: 
                print(f"✅ 状态已稳定！当前高度: {self.current_position[2]:.2f}m，交由 AI 接管")
                break
            rate.sleep()

        self.control_mode = "VELOCITY"
        self.current_action = np.array([0.0, 0.0, 0.0])
        return self.current_position.astype(np.float32), {}

    def step(self, action):
        self.current_action = action
        rospy.sleep(0.1)

        obs = self.current_position.astype(np.float32)
        dist = np.linalg.norm(obs - self.target_pos)
        
        # 核心改动：生存奖励 + 距离惩罚
        # 只要没死，每步给 1 分奖励；但距离目标越远扣分越多
        reward = 1.0 - (dist * 0.5) 

        terminated = False
        if obs[2] < 0.2 or dist > 10.0:
            reward = -100.0 # 保持巨大的死亡惩罚
            terminated = True
            
        return obs, reward, terminated, False, {}