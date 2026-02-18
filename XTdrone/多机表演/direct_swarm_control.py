#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist, PoseStamped
from mavros_msgs.msg import State
from mavros_msgs.srv import CommandBool, SetMode
import time

class DirectSwarmCommander:
    def __init__(self):
        rospy.init_node('direct_swarm_control', anonymous=True)
        self.uav_num = 3
        self.vel_pubs = []
        self.arming_srvs = []
        self.set_mode_srvs = []
        self.states = [None] * self.uav_num

        print("📡 初始化 MAVROS 直连接口...")
        for i in range(self.uav_num):
            # 1. 速度控制 (直接发给 MAVROS，不走 XTDrone)
            # 注意: 使用 body 坐标系 cmd_vel_unstamped
            self.vel_pubs.append(rospy.Publisher(f'/iris_{i}/mavros/setpoint_velocity/cmd_vel_unstamped', Twist, queue_size=10))
            
            # 2. 服务客户端
            rospy.wait_for_service(f'/iris_{i}/mavros/cmd/arming')
            self.arming_srvs.append(rospy.ServiceProxy(f'/iris_{i}/mavros/cmd/arming', CommandBool))
            
            rospy.wait_for_service(f'/iris_{i}/mavros/set_mode')
            self.set_mode_srvs.append(rospy.ServiceProxy(f'/iris_{i}/mavros/set_mode', SetMode))
            
            # 3. 状态订阅
            rospy.Subscriber(f'/iris_{i}/mavros/state', State, self.state_cb, callback_args=i)
            print(f"   > iris_{i} 接口就绪")

        time.sleep(1)

    def state_cb(self, msg, uav_id):
        self.states[uav_id] = msg

    def send_vel(self, uav_id, vx, vy, vz):
        vel = Twist()
        vel.linear.x = vx
        vel.linear.y = vy
        vel.linear.z = vz
        self.vel_pubs[uav_id].publish(vel)

    def run(self):
        rate = rospy.Rate(20)
        
        # --- 步骤 1: 预发送设定点 (防止切模式被拒) ---
        print("\n⏳ [1/4] 发送 0 速度流 (5秒)...")
        for _ in range(100):
            for i in range(self.uav_num):
                self.send_vel(i, 0, 0, 0)
            rate.sleep()

        # --- 步骤 2: 切换 OFFBOARD ---
        print("\n🔄 [2/4] 尝试切换 OFFBOARD...")
        for i in range(self.uav_num):
            try:
                # 持续发送 setpoints 的同时切模式
                self.send_vel(i, 0, 0, 0) 
                res = self.set_mode_srvs[i](custom_mode="OFFBOARD")
                print(f"   > iris_{i} OFFBOARD 请求: {'成功' if res.mode_sent else '失败'}")
            except rospy.ServiceException as e:
                print(f"   > iris_{i} 服务调用失败: {e}")

        # --- 步骤 3: 解锁 (ARM) ---
        print("\n🔓 [3/4] 尝试解锁 (ARM)...")
        for i in range(self.uav_num):
            try:
                self.send_vel(i, 0, 0, 0)
                res = self.arming_srvs[i](value=True)
                print(f"   > iris_{i} 解锁请求: {'成功' if res.success else '失败'}")
            except rospy.ServiceException as e:
                print(f"   > iris_{i} 服务调用失败: {e}")

        # --- 步骤 4: 起飞 ---
        print("\n⬆️ [4/4] 起飞! (持续发送上升指令)...")
        start_time = time.time()
        while time.time() - start_time < 8.0:
            for i in range(self.uav_num):
                # 发送 Z 轴速度 0.7 m/s
                self.send_vel(i, 0, 0, 0.7)
                
                # 双重保险: 如果掉出 OFFBOARD，再次尝试切换
                if self.states[i] and self.states[i].mode != "OFFBOARD":
                     self.set_mode_srvs[i](custom_mode="OFFBOARD")
                
                # 双重保险: 如果未解锁，再次尝试解锁
                if self.states[i] and not self.states[i].armed:
                     self.arming_srvs[i](value=True)
                     
            rate.sleep()

        print("🎉 脚本结束，悬停中...")
        while not rospy.is_shutdown():
            for i in range(self.uav_num):
                self.send_vel(i, 0, 0, 0)
            rate.sleep()

if __name__ == '__main__':
    try:
        commander = DirectSwarmCommander()
        commander.run()
    except rospy.ROSInterruptException:
        pass
