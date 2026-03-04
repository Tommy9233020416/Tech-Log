import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist, PoseStamped
from mavros_msgs.msg import State
import time

class SwarmTester:
    def __init__(self):
        rospy.init_node('swarm_hello_world', anonymous=True)
        self.uav_num = 3
        self.cmd_pubs = []
        self.vel_pubs = []
        
        # 状态记录
        self.uav_states = [None] * self.uav_num
        self.uav_poses = [None] * self.uav_num
        
        print("📡 [1/5] 初始化通信接口...")
        for i in range(self.uav_num):
            # 1. 指令发布
            self.cmd_pubs.append(rospy.Publisher(f'/xtdrone/iris_{i}/cmd', String, queue_size=10))
            self.vel_pubs.append(rospy.Publisher(f'/xtdrone/iris_{i}/cmd_vel_flu', Twist, queue_size=10))
            
            # 2. [关键新增] 状态订阅 (用于检查连接)
            rospy.Subscriber(f'/iris_{i}/mavros/state', State, self.state_cb, callback_args=i)
            # 3. [关键新增] 位置订阅 (用于确认 EKF 就绪)
            rospy.Subscriber(f'/iris_{i}/mavros/local_position/pose', PoseStamped, self.pose_cb, callback_args=i)
            
        print("⏳ [2/5] 等待 3 架无人机连接 (Heartbeat & GPS)...")
        self.wait_for_connection()

    def state_cb(self, msg, uav_id):
        self.uav_states[uav_id] = msg

    def pose_cb(self, msg, uav_id):
        self.uav_poses[uav_id] = msg

    def wait_for_connection(self):
        """严格的起飞前检查"""
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            ready_count = 0
            for i in range(self.uav_num):
                # 检查1: MAVROS 是否连接
                connected = self.uav_states[i] is not None and self.uav_states[i].connected
                # 检查2: 是否有位置数据 (说明 EKF 正常)
                has_pose = self.uav_poses[i] is not None
                
                if connected and has_pose:
                    ready_count += 1
            
            # 打印进度
            print(f"\r   >>> 就绪状态: {ready_count}/{self.uav_num} 架飞机已连接...", end="")
            
            if ready_count == self.uav_num:
                print("\n✅ 所有飞机连接确认！EKF 健康！")
                break
            rate.sleep()

    def broadcast_vel(self, x=0, y=0, z=0):
        vel = Twist()
        vel.linear.x = x
        vel.linear.y = y
        vel.linear.z = z
        for pub in self.vel_pubs:
            pub.publish(vel)

    def broadcast_cmd(self, cmd):
        for pub in self.cmd_pubs:
            pub.publish(cmd)

    def run_test(self):
        rate = rospy.Rate(20)
        
        # --- 步骤 0: 预热 (发送速度 0) ---
        print("\n⚡ [3/5] 发送预备信号 (建立 OFFBOARD 信用)...")
        for i in range(50): # 2.5秒
            self.broadcast_vel(0, 0, 0)
            self.broadcast_cmd("OFFBOARD")
            rate.sleep()

        # --- 步骤 1: 解锁 ---
        print("🔓 [4/5] 全员解锁 (ARM)...")
        for i in range(40): # 持续 2 秒发送解锁，防止丢包
            self.broadcast_vel(0, 0, 0)
            self.broadcast_cmd("ARM")
            rate.sleep()

        # --- 步骤 2: 起飞 ---
        print("⬆️ [5/5] 全员起飞 (高度 1m)...")
        start_time = time.time()
        while time.time() - start_time < 5.0: # 5秒上升
            self.broadcast_vel(0, 0, 0.6) # 稍微加大油门
            self.broadcast_cmd("OFFBOARD") # 持续维持模式
            rate.sleep()

        # --- 步骤 3: 悬停展示 ---
        print("⏸️ 空中悬停保持...")
        start_time = time.time()
        while time.time() - start_time < 3.0:
            self.broadcast_vel(0, 0, 0)
            rate.sleep()

        # --- 步骤 4: 降落 ---
        print("⬇️ 任务结束，自动降落...")
        for i in range(20):
            self.broadcast_cmd("AUTO.LAND")
            rate.sleep()

if __name__ == '__main__':
    try:
        tester = SwarmTester()
        tester.run_test()
    except rospy.ROSInterruptException:
        pass