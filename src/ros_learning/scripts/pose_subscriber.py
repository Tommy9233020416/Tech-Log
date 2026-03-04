#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from turtlesim.msg import Pose # 注意这里不是 geometry_msgs 了

# --- 核心概念：回调函数 (Callback) ---
# 这是一个“被动触发”的函数。
# 你的主程序不需要调用它。
# 每当海龟在 /turtle1/pose 话题发一条消息，ROS 就会自动跳过来执行一次这个函数。
def pose_callback(msg):
    # msg 就是接收到的数据包
    rospy.loginfo("海龟当前坐标: x=%.2f, y=%.2f", msg.x, msg.y)
    
    # 简单的逻辑判断
    if msg.x > 9.0:
        rospy.logwarn("警报：即将撞墙！")

def pose_subscriber():
    # 1. 初始化节点
    rospy.init_node('pose_subscriber', anonymous=True)

    # 2. 创建订阅者
    # 语法：rospy.Subscriber(话题名, 消息类型, 回调函数)
    rospy.Subscriber("/turtle1/pose", Pose, pose_callback)

    # 3. 循环等待 (Spin)
    # 这行代码的意思是：“程序卡在这里别退出，一直活着听消息，直到我按 Ctrl+C”
    # 如果没有这行，程序运行完上面两行就直接结束了，根本来不及收消息。
    rospy.spin()

if __name__ == '__main__':
    pose_subscriber()