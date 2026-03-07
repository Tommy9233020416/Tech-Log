#!/usr/bin/env python3
import rospy
import cv2
import numpy as np
import os
import time
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from gazebo_msgs.msg import ModelStates
from geometry_msgs.msg import PoseStamped
import tf.transformations as tf_trans

class DataCollector:
    def __init__(self):
        rospy.init_node('data_collector', anonymous=True)
        self.bridge = CvBridge()
        
        # Paths
        self.base_path = '/root/ros_ws/src/rl_drone_yolo/scripts/dataset'
        self.img_path = os.path.join(self.base_path, 'images/train')
        self.lbl_path = os.path.join(self.base_path, 'labels/train')
        os.makedirs(self.img_path, exist_ok=True)
        os.makedirs(self.lbl_path, exist_ok=True)
        
        # Params
        self.camera_topic = '/iris/usb_cam/image_raw'
        self.vehicle_name = 'iris'
        self.pad_name = 'aruco_pad'
        
        # Camera Info (Matches iris_yolo/fpv_cam)
        self.img_w = 320
        self.img_h = 240
        self.fov = 1.047 # 60 deg
        
        # State
        self.latest_image = None
        self.iris_pose = None
        self.pad_pose = None
        self.count = 0
        
        # Subscribers
        rospy.Subscriber(self.camera_topic, Image, self.image_cb)
        rospy.Subscriber('/gazebo/model_states', ModelStates, self.model_cb)
        
        rospy.loginfo("Data Collector Initialized. Waiting for data...")

    def image_cb(self, msg):
        self.latest_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")

    def model_cb(self, msg):
        try:
            iris_idx = msg.name.index(self.vehicle_name)
            pad_idx = msg.name.index(self.pad_name)
            self.iris_pose = msg.pose[iris_idx]
            self.pad_pose = msg.pose[pad_idx]
        except ValueError:
            pass

    def get_yolo_label(self):
        if self.iris_pose is None or self.pad_pose is None:
            return None
            
        # 1. Transform pad position to iris body frame
        # For simplicity in iris_yolo, camera is rotated 90deg down.
        # Body frame (FLU): X-front, Y-left, Z-up
        # Camera frame (pointing down): Z_c is down (-Z_b), X_c is front (X_b), Y_c is right (-Y_b)
        
        dx = self.pad_pose.position.x - self.iris_pose.position.x
        dy = self.pad_pose.position.y - self.iris_pose.position.y
        dz = self.pad_pose.position.z - self.iris_pose.position.z
        
        # Get iris orientation
        q = [self.iris_pose.orientation.x, self.iris_pose.orientation.y, 
             self.iris_pose.orientation.z, self.iris_pose.orientation.w]
        inv_q = tf_trans.quaternion_inverse(q)
        
        # Relative vector in world frame
        rel_pos_w = [dx, dy, dz, 0]
        # Rotate to body frame
        rel_pos_b = tf_trans.quaternion_multiply(
            tf_trans.quaternion_multiply(inv_q, rel_pos_w),
            q
        )
        bx, by, bz = rel_pos_b[:3]
        
        # Camera is at (0,0,-0.05) in body frame, looking down.
        # In Camera frame: 
        # Zc = -bz - 0.05 (Distance from camera to pad)
        # Xc = bx (Front)
        # Yc = -by (Right)
        
        zc = -bz - 0.05
        if zc <= 0.1: return None # Too close or behind
        
        # Project to image (Pinhole model)
        # f = (width/2) / tan(fov/2)
        f = (self.img_w / 2.0) / np.tan(self.fov / 2.0)
        
        # Drone Body Frame (FLU): bx (front), by (left), bz (up)
        # Camera Frame (OpenCV style looking down): 
        # Zc = -bz (down)
        # Xc = -by (right is -left)
        # Yc = -bx (down is -front)
        
        nx = f * ((-by) / zc)
        ny = f * ((-bx) / zc)
        
        # Pixel coords (center is w/2, h/2)
        px = self.img_w / 2.0 + nx
        py = self.img_h / 2.0 + ny
        
        # Pad size in Gazebo is 1.0m x 1.0m
        # Approximate box size in pixels
        box_w = f * (1.0 / zc)
        box_h = f * (1.0 / zc)
        
        # Normalize for YOLO (0-1)
        x_center = px / self.img_w
        y_center = py / self.img_h
        width = box_w / self.img_w
        height = box_h / self.img_h
        
        # Check if in bounds
        if 0 < x_center < 1 and 0 < y_center < 1:
            return f"0 {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"
        return None

    def capture(self):
        if self.latest_image is None: return
        
        label = self.get_yolo_label()
        if label:
            timestamp = int(time.time() * 1000)
            img_filename = f"pad_{timestamp}.jpg"
            lbl_filename = f"pad_{timestamp}.txt"
            
            cv2.imwrite(os.path.join(self.img_path, img_filename), self.latest_image)
            with open(os.path.join(self.lbl_path, lbl_filename), 'w') as f:
                f.write(label)
            
            self.count += 1
            if self.count % 10 == 0:
                rospy.loginfo(f"Captured {self.count} samples...")

if __name__ == '__main__':
    collector = DataCollector()
    rate = rospy.Rate(5) # 5fps to avoid duplicates
    while not rospy.is_shutdown():
        collector.capture()
        rate.sleep()
