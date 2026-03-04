import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import time

def run_test():
    # 1. 初始化节点
    rospy.init_node('auto_test_pilot', anonymous=True)
    
    # 2. 定义发布者
    # cmd_pub: 发送字符串指令 (解锁、切模式、降落)
    cmd_pub = rospy.Publisher('/xtdrone/iris_0/cmd', String, queue_size=3)
    # vel_pub: 发送速度指令 (前后左右上下移动)
    vel_pub = rospy.Publisher('/xtdrone/iris_0/cmd_vel_flu', Twist, queue_size=3)
    
    # 设置发送频率 (20Hz)
    rate = rospy.Rate(20) 
    
    print("----------------------------------------")
    print("🤖 自动飞行测试脚本已启动")
    print("⏳ 等待 ROS 通信链路建立 (2秒)...")
    time.sleep(2)

    # --- 阶段 1: 解锁与起飞 ---
    print("\n🚀 [1/4] 请求解锁 (ARM) & 外部控制 (OFFBOARD)...")
    # 连续发送几次指令，确保不丢包
    for i in range(10):
        cmd_pub.publish("OFFBOARD")
        cmd_pub.publish("ARM")
        rate.sleep()
    
    print("⬆️ [2/4] 起飞中 (向上速度 0.6 m/s, 持续 4秒)...")
    # 创建起飞速度指令
    takeoff_cmd = Twist()
    takeoff_cmd.linear.z = 2.0  # 向上 0.6 m/s
    
    start_time = time.time()
    while time.time() - start_time < 4.0:
        vel_pub.publish(takeoff_cmd)
        rate.sleep()

    # --- 阶段 2: 空中动作 ---
    print("🔄 [3/4] 执行动作: 悬停并旋转 (角速度 0.8 rad/s)...")
    rotate_cmd = Twist()
    rotate_cmd.angular.z = 2  # 逆时针旋转
    # 稍微给一点向上的力抵抗重力漂移（可选，视仿真物理而定）
    rotate_cmd.linear.z = 0.65 
    
    start_time = time.time()
    while time.time() - start_time < 5.0:
        vel_pub.publish(rotate_cmd)
        rate.sleep()

    # --- 阶段 3: 降落 ---
    print("\n⬇️ [4/4] 任务完成，自动降落 (LAND)...")
    # 发送降落指令，通信脚本会将其转换为 AUTO.LAND 模式
    cmd_pub.publish("AUTO.LAND")
    
    # 防止程序过早退出导致指令没发出去
    time.sleep(1)
    print("✅ 测试脚本结束")
    print("----------------------------------------")

if __name__ == '__main__':
    try:
        run_test()
    except rospy.ROSInterruptException:
        pass