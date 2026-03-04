#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseStamped, Twist
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
import time

class DebugCircler:
    def __init__(self):
        rospy.init_node('debug_circle_node', anonymous=True)
        
        self.bridge = CvBridge()
        self.local_pose_sub = rospy.Subscriber("/iris_0/mavros_manual/local_position/pose", PoseStamped, self.pose_callback)
        self.image_sub = rospy.Subscriber("/stereo/left/image_raw", Image, self.image_callback)
        self.cmd_pub = rospy.Publisher('/xtdrone/iris_0/cmd', String, queue_size=3)
        self.vel_pub = rospy.Publisher('/xtdrone/iris_0/cmd_vel_flu', Twist, queue_size=3)
        
        # 状态量
        self.current_z = 0.0
        self.got_pose = False
        self.is_tracking = False # 是否看到了目标
        
        # 参数
        self.kp_yaw = 0.003
        self.kp_dist = 0.015
        self.kp_z = 1.0
        self.target_height = 1.4
        self.target_radius = 60
        self.side_speed = -0.5  # [修改] 加大侧飞速度
        
        print("⏳ 等待高度计数据...")
        while not self.got_pose and not rospy.is_shutdown():
            time.sleep(0.1)
        
        self.takeoff_closed_loop()

    def pose_callback(self, msg):
        self.current_z = msg.pose.position.z
        self.got_pose = True

    def takeoff_closed_loop(self):
        print("🚀 起飞初始化...")
        rate = rospy.Rate(20)
        for i in range(20):
            self.cmd_pub.publish("OFFBOARD")
            self.cmd_pub.publish("ARM")
            rate.sleep()
            
        print("⬆️ 闭环上升中...")
        while abs(self.current_z - self.target_height) > 0.1 and not rospy.is_shutdown():
            vel = Twist()
            vel.linear.z = self.kp_z * (self.target_height - self.current_z)
            vel.linear.z = max(min(vel.linear.z, 0.8), -0.8)
            self.vel_pub.publish(vel)
            rate.sleep()
            
        print("✅ 高度稳定，开始视觉逻辑")

    def image_callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError:
            return

        rows, cols, _ = cv_image.shape
        center_x = cols / 2

        # 颜色识别
        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        lower_yellow = np.array([15, 80, 80])
        upper_yellow = np.array([45, 255, 255])
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        vel_cmd = Twist()
        
        # --- 高度始终闭环 ---
        vel_cmd.linear.z = self.kp_z * (self.target_height - self.current_z)

        # 状态文本颜色
        status_color = (0, 0, 255) # 默认红色 (SEARCHING)
        status_text = "SEARCHING"

        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            
            if radius > 10: 
                self.is_tracking = True
                status_color = (0, 255, 0) # 绿色 (TRACKING)
                status_text = f"TRACKING (R={int(radius)})"
                
                # 画出目标
                cv2.circle(cv_image, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.line(cv_image, (int(center_x), int(rows//2)), (int(x), int(y)), (255, 0, 0), 2)

                # 计算控制量
                error_yaw = center_x - x
                error_dist = self.target_radius - radius
                
                vel_cmd.angular.z = self.kp_yaw * error_yaw
                vel_cmd.linear.x = self.kp_dist * error_dist
                vel_cmd.linear.y = self.side_speed  # [关键] 侧飞指令

                # 限制幅度
                vel_cmd.linear.x = max(min(vel_cmd.linear.x, 0.5), -0.5)

                # 在屏幕上打印指令值 (HUD)
                cv2.putText(cv_image, f"CMD_X (Dist): {vel_cmd.linear.x:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                cv2.putText(cv_image, f"CMD_Y (Side): {vel_cmd.linear.y:.2f}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                cv2.putText(cv_image, f"CMD_Yaw: {vel_cmd.angular.z:.2f}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

            else:
                self.is_tracking = False
                vel_cmd.angular.z = 0.3
        else:
            self.is_tracking = False
            vel_cmd.angular.z = 0.3 # 没找到，原地转圈找
            
        self.vel_pub.publish(vel_cmd)
        
        # 左上角显示大状态
        cv2.putText(cv_image, f"MODE: {status_text}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2)
        
        cv2.imshow("Debug HUD", cv_image)
        cv2.waitKey(3)

if __name__ == '__main__':
    try:
        DebugCircler()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
    finally:
        cv2.destroyAllWindows()