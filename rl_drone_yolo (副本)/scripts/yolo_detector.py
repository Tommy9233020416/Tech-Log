#!/usr/bin/env python3
import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from geometry_msgs.msg import Point
from ultralytics import YOLO

class YOLODetector:
    def __init__(self):
        rospy.init_node('yolo_detector', anonymous=True)
        
        # Parameters
        self.image_topic = rospy.get_param('~image_topic', '/camera/image_raw')
        self.model_path = rospy.get_param('~model_path', '/root/ros_ws/src/rl_drone_yolo/scripts/best_pad.pt')
        self.conf_threshold = rospy.get_param('~conf_threshold', 0.2)
        
        # Load YOLO model
        self.model = YOLO(self.model_path)
        
        # Bridge for ROS to OpenCV
        self.bridge = CvBridge()
        
        # Publisher for detection result (relative x, y in [-1, 1], z is diameter if detected)
        self.detection_pub = rospy.Publisher('/rl_drone/yolo/detection', Point, queue_size=1)
        
        # Publisher for debug visualization
        self.debug_pub = rospy.Publisher('/rl_drone/yolo/debug_image', Image, queue_size=1)
        
        # Subscriber
        self.image_sub = rospy.Subscriber(self.image_topic, Image, self.image_callback)
        
        rospy.loginfo(f"YOLO Detector initialized. Subscribed to {self.image_topic}")

    def image_callback(self, msg):
        try:
            # Convert ROS Image to OpenCV format
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            
            # Predict
            results = self.model.predict(cv_image, conf=self.conf_threshold, verbose=False)
            
            h, w, _ = cv_image.shape
            
            # For this task, we assume we want to find the largest object or a specific class
            # Since we are looking for a landing pad, let's find the most prominent detection
            # or filter by class if necessary.
            
            best_det = None
            max_area = 0
            
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    # Filter by class if needed, e.g., if we trained for 'pad'
                    # For now, let's just find the most likely detection
                    
                    # Convert to xyxy
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    conf = box.conf[0].item()
                    cls = int(box.cls[0].item())
                    area = (x2 - x1) * (y2 - y1)
                    
                    if area > max_area:
                        max_area = area
                        best_det = (x1, y1, x2, y2)
            
            if best_det:
                x1, y1, x2, y2 = best_det
                cx = (x1 + x2) / 2.0
                cy = (y1 + y2) / 2.0
                
                # Normalize coordinates to [-1, 1]
                # (cx - w/2) / (w/2) -> 2*cx/w - 1
                nx = (2.0 * cx / w) - 1.0
                ny = (2.0 * cy / h) - 1.0
                
                # We can use the width/height of box as a proxy for distance if needed
                # For now just send normalized x, y
                det_msg = Point()
                det_msg.x = nx
                det_msg.y = ny
                det_msg.z = max_area / (w * h) # Relative area
                self.detection_pub.publish(det_msg)
                
                # Draw for debug (optional, could be gated by param)
                cv2.rectangle(cv_image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.circle(cv_image, (int(cx), int(cy)), 5, (0, 0, 255), -1)
                cv2.putText(cv_image, f"Pad: {nx:.2f},{ny:.2f}", (int(x1), int(y1)-10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Publish annotated image for debugging
            try:
                debug_msg = self.bridge.cv2_to_imgmsg(cv_image, "bgr8")
                self.debug_pub.publish(debug_msg)
            except Exception as e:
                rospy.logerr(f"Debug Image Publish Error: {e}")
            
        except Exception as e:
            rospy.logerr(f"YOLO Error: {e}")

if __name__ == '__main__':
    try:
        detector = YOLODetector()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
