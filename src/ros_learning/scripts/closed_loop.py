#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class TurtleStopper:
    def __init__(self):
        rospy.init_node('turtle_stopper', anonymous=True)
        
        # 1. 创建发布者 (控制速度)
        self.pub = rospy.Publisher('/turtle2/cmd_vel', Twist, queue_size=10)
        
        # 2. 创建订阅者 (监听位置)
        self.sub = rospy.Subscriber('/turtle2/pose', Pose, self.pose_callback)
        
        self.pose = Pose() # 用来存储当前位置
        self.rate = rospy.Rate(10)

    def pose_callback(self, msg):
        # 只要有位置更新，就存到 self.pose 里
        self.pose = msg

    def move(self):
        vel_msg = Twist()
        
        while not rospy.is_shutdown():
            # --- 核心逻辑 ---
            # 如果 x 坐标小于 8.0，就全速前进
            if self.pose.x < 8.0:
                vel_msg.linear.x = 2.0
                rospy.loginfo("冲鸭！当前位置: %.2f", self.pose.x)
            else:
                # 否则（到了墙边），立即停车
                vel_msg.linear.x = -2.0
                while self.pose.x > 5.0 and not rospy.is_shutdown():
                    vel_msg.linear.x = -2.0
                    rospy.loginfo("倒车！当前位置: %.2f", self.pose.x)
                    self.pub.publish(vel_msg)
                    self.rate.sleep()
                rospy.logwarn("到达终点，停车！")
            
            # 发送指令
            self.pub.publish(vel_msg)
            self.rate.sleep()

if __name__ == '__main__':
    try:
        stopper = TurtleStopper()
        stopper.move()
    except rospy.ROSInterruptException:
        pass