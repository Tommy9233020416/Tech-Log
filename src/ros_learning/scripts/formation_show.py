import rospy
import math
import time
import numpy as np
from geometry_msgs.msg import Twist, PoseStamped
from mavros_msgs.msg import State
from mavros_msgs.srv import CommandBool, SetMode

class FormationShow:
    def __init__(self):
        rospy.init_node('formation_show', anonymous=True)
        self.uav_num = 3
        self.vel_pubs = []
        self.arming_srvs = []
        self.set_mode_srvs = []
        
        # 状态容器
        self.states = [None] * self.uav_num
        self.poses = [None] * self.uav_num # [x, y, z]

        print("📡 初始化编队控制接口...")
        for i in range(self.uav_num):
            # 1. 速度控制发布
            self.vel_pubs.append(rospy.Publisher(f'/iris_{i}/mavros/setpoint_velocity/cmd_vel_unstamped', Twist, queue_size=10))
            
            # 2. 服务客户端
            rospy.wait_for_service(f'/iris_{i}/mavros/cmd/arming')
            self.arming_srvs.append(rospy.ServiceProxy(f'/iris_{i}/mavros/cmd/arming', CommandBool))
            rospy.wait_for_service(f'/iris_{i}/mavros/set_mode')
            self.set_mode_srvs.append(rospy.ServiceProxy(f'/iris_{i}/mavros/set_mode', SetMode))
            
            # 3. 订阅状态与位置 (核心升级)
            rospy.Subscriber(f'/iris_{i}/mavros/state', State, self.state_cb, callback_args=i)
            rospy.Subscriber(f'/iris_{i}/mavros/local_position/pose', PoseStamped, self.pose_cb, callback_args=i)
            
            print(f"   > iris_{i} 就绪")
        
        time.sleep(1)

    # --- 回调函数 ---
    def state_cb(self, msg, uav_id):
        self.states[uav_id] = msg

    def pose_cb(self, msg, uav_id):
        # 记录当前位置 [x, y, z]
        self.poses[uav_id] = [msg.pose.position.x, msg.pose.position.y, msg.pose.position.z]

    # --- 核心控制算法：P控制器 ---
    def move_to_target(self, uav_id, target_x, target_y, target_z, kp=1.0):
        """
        根据目标位置计算速度，实现平滑移动
        """
        if self.poses[uav_id] is None:
            return # 没有位置数据时不动

        curr_x, curr_y, curr_z = self.poses[uav_id]

        # 计算误差
        err_x = target_x - curr_x
        err_y = target_y - curr_y
        err_z = target_z - curr_z

        # P控制计算速度 (速度 = 误差 * 比例系数)
        vel = Twist()
        vel.linear.x = max(min(err_x * kp, 1.5), -1.5) # 限速 1.5 m/s
        vel.linear.y = max(min(err_y * kp, 1.5), -1.5)
        vel.linear.z = max(min(err_z * kp, 1.0), -1.0) # 垂直限速 1.0 m/s

        self.vel_pubs[uav_id].publish(vel)
        
        # 返回是否到达目标 (误差小于阈值)
        dist = math.sqrt(err_x**2 + err_y**2 + err_z**2)
        return dist < 0.2

    # --- 基础指令封装 ---
    def send_vel(self, uav_id, vx, vy, vz):
        vel = Twist()
        vel.linear.x = vx; vel.linear.y = vy; vel.linear.z = vz
        self.vel_pubs[uav_id].publish(vel)

    def arm_and_takeoff(self):
        print("\n⚡ [1/3] 预热与解锁...")
        # 1. 发送心跳流
        for _ in range(50):
            for i in range(self.uav_num): self.send_vel(i, 0, 0, 0)
            time.sleep(0.05)
        
        # 2. 切换模式与解锁
        for i in range(self.uav_num):
            try:
                self.set_mode_srvs[i](custom_mode="OFFBOARD")
                self.arming_srvs[i](value=True)
                print(f"   > iris_{i} 解锁成功")
            except: pass

        print("⬆️ [2/3] 同步起飞至 2米高度...")
        start_t = time.time()
        while time.time() - start_t < 8.0:
            for i in range(self.uav_num):
                # 利用 P 控制器稳定爬升
                self.move_to_target(i, self.poses[i][0], self.poses[i][1], 2.0) 
            time.sleep(0.05)

    def run_show(self):
        self.arm_and_takeoff()
        
        print("\n🎪 [3/3] 表演开始：旋转大三角 (Rotating Triangle)")
        
        # --- 设定圆心与半径 ---
        center = [0, 0] # 旋转中心
        radius = 3.0    # 旋转半径
        omega = 0.5     # 角速度 (弧度/秒)
        total_time = 30 # 表演时长 (秒)
        
        # 三架飞机的相位差 (120度 = 2pi/3)
        phases = [0, 2*math.pi/3, 4*math.pi/3]
        
        start_t = time.time()
        while not rospy.is_shutdown():
            t = time.time() - start_t
            if t > total_time: break
            
            for i in range(self.uav_num):
                if self.poses[i] is None: continue
                
                # 计算每一刻的目标位置 (圆周运动公式)
                # x = r * cos(wt + phi)
                # y = r * sin(wt + phi)
                target_x = center[0] + radius * math.cos(omega * t + phases[i])
                target_y = center[1] + radius * math.sin(omega * t + phases[i])
                target_z = 2.0 # 保持高度
                
                # 执行控制
                self.move_to_target(i, target_x, target_y, target_z, kp=1.5)
            
            # 打印进度条
            print(f"\r   ⏳ 正在旋转... {t:.1f}/{total_time}s", end="")
            time.sleep(0.05)

        print("\n⬇️ 表演结束，同步降落...")
        for i in range(self.uav_num):
            try:
                self.set_mode_srvs[i](custom_mode="AUTO.LAND")
            except: pass
        time.sleep(5)

if __name__ == '__main__':
    try:
        shower = FormationShow()
        shower.run_show()
    except rospy.ROSInterruptException:
        pass