#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist

def velocity_publisher():
    # 1. 初始化节点
    rospy.init_node('velocity_publisher_vscode', anonymous=True)
    
    # 2. 创建发布者
    turtle_vel_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    
   
    # 3. 设置循环频率
    rate = rospy.Rate(10) 
    
    while not rospy.is_shutdown():
        # 4. 初始化 Twist 消息
        vel_msg = Twist()
        
        # --- 在这里修改数值体验不同轨迹 ---
        vel_msg.linear.x = 2.0   # 线速度
        vel_msg.angular.z = 1.8  # 角速度 (变大这个值，圆会变小)
        # -------------------------------
        
        # 5. 发布并打印日志
        turtle_vel_pub.publish(vel_msg)
        rospy.loginfo("VS Code 发送指令: [%0.2f m/s, %0.2f rad/s]", 
                      vel_msg.linear.x, vel_msg.angular.z)
        
        rate.sleep()

if __name__ == '__main__':
    try:
        velocity_publisher()
    except rospy.ROSInterruptException:
        pass