#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import math
import random
import time

def move_target():
    rospy.init_node('target_mover', anonymous=True)
    pub = rospy.Publisher('/target/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10) # 10hz

    # Non-linear chaotic motion parameters
    t = 0.0
    
    # Store origin to bounce back if it goes too far
    # Since we can't easily subscribe to its own odom in this simple script 
    # without adding complexity, we'll try to keep the velocities zero-mean over time
    # by using sine waves of different frequencies.
    
    freq_x1 = 0.2
    freq_x2 = 0.5
    freq_y1 = 0.3
    freq_y2 = 0.7
    
    while not rospy.is_shutdown():
        twist = Twist()
        
        # generate pseudo-random / non-linear motion using sum of sines
        # scale down the velocity to prevent it from escaping the 10m area too fast
        vx = 0.5 * math.sin(t * freq_x1) + 0.3 * math.sin(t * freq_x2)
        vy = 0.4 * math.sin(t * freq_y1) + 0.6 * math.cos(t * freq_y2)
        
        # occasionally add random bursts
        if random.random() < 0.02:
            vx += random.uniform(-1.0, 1.0)
            vy += random.uniform(-1.0, 1.0)
            
        twist.linear.x = vx
        twist.linear.y = vy
        twist.linear.z = 0.0
        
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = random.uniform(-0.2, 0.2) # slow random rotation
        
        pub.publish(twist)
        t += 0.1
        rate.sleep()

if __name__ == '__main__':
    try:
        move_target()
    except rospy.ROSInterruptException:
        pass
