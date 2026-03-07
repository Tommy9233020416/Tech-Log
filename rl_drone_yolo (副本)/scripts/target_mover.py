#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from gazebo_msgs.msg import ModelStates
import math
import random

class TargetMover:
    def __init__(self):
        rospy.init_node('target_mover', anonymous=True)
        
        # Accept parameters for Multi-UAV segregation
        self.pad_name = rospy.get_param('~pad_name', 'aruco_pad')
        cmd_topic = rospy.get_param('~cmd_topic', 'target/cmd_vel')
        
        self.pub = rospy.Publisher(cmd_topic, Twist, queue_size=10)
        self.rate = rospy.Rate(10) # 10hz
        
        self.anchor_x = None
        self.anchor_y = None
        self.current_x = None
        self.current_y = None
        
        # Subscribe to gazebo model states to get the true position
        rospy.Subscriber("/gazebo/model_states", ModelStates, self.model_cb)
        
    def model_cb(self, msg):
        try:
            idx = msg.name.index(self.pad_name)
            x = msg.pose[idx].position.x
            y = msg.pose[idx].position.y
            
            # If the pad teleports (distance > 1.0m in 0.1s), update the anchor
            if self.current_x is None:
                self.anchor_x = x
                self.anchor_y = y
            else:
                dist = math.hypot(x - self.current_x, y - self.current_y)
                if dist > 1.0:
                    self.anchor_x = x
                    self.anchor_y = y
                    
            self.current_x = x
            self.current_y = y
        except ValueError:
            pass

    def run(self):
        t = 0.0
        
        freq_x1 = 0.1
        freq_x2 = 0.2
        freq_y1 = 0.15
        freq_y2 = 0.3
        
        while not rospy.is_shutdown():
            twist = Twist()
            
            # Sinusoidal velocities (Further reduced speed)
            vx = (0.1 * math.sin(t * freq_x1) + 0.05 * math.sin(t * freq_x2)) / 2.0
            vy = (0.08 * math.sin(t * freq_y1) + 0.12 * math.cos(t * freq_y2)) / 2.0
            
            # Fixed anchor at origin (0,0) as per user request
            anchor_x, anchor_y = 0.0, 0.0
            
            if self.current_x is not None:
                dx = self.current_x - anchor_x
                dy = self.current_y - anchor_y
                
                k_pull = 0.5
                # Boundary enforcement at 1.0m
                if abs(dx) > 0.8:
                    vx -= k_pull * dx
                if abs(dy) > 0.8:
                    vy -= k_pull * dy
                    
                if dx > 1.0 and vx > 0: vx = -0.3
                if dx < -1.0 and vx < 0: vx = 0.3
                if dy > 1.0 and vy > 0: vy = -0.3
                if dy < -1.0 and vy < 0: vy = 0.3
                
            if random.random() < 0.02:
                vx += random.uniform(-0.06, 0.06)
                vy += random.uniform(-0.06, 0.06)
                
            twist.linear.x = vx
            twist.linear.y = vy
            twist.linear.z = 0.0
            
            twist.angular.x = 0.0
            twist.angular.y = 0.0
            twist.angular.z = random.uniform(-0.1, 0.1)
            
            self.pub.publish(twist)
            t += 0.1
            self.rate.sleep()

if __name__ == '__main__':
    try:
        mover = TargetMover()
        mover.run()
    except rospy.ROSInterruptException:
        pass
