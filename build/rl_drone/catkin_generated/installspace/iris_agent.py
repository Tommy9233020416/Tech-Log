#!/usr/bin/env python3
import rospy
import math
import time
from geometry_msgs.msg import Twist, PoseStamped, TwistStamped
from mavros_msgs.msg import State, PositionTarget
from mavros_msgs.srv import CommandBool, SetMode
from gazebo_msgs.msg import ModelStates

class IrisAgent:
    def __init__(self):
        rospy.init_node('iris_agent', anonymous=True)

        # MAVROS state
        self.state = State()
        self.pose = PoseStamped()
        self.vel = TwistStamped()
        self.target_dx = 0.0
        self.target_dy = 0.0
        self.target_detected = False
        
        # Gazebo model states (for mock Aruco detection)
        # In a real setup, this would be an image pipeline
        self.models = ModelStates()
        
        # Publishers and Subscribers
        rospy.Subscriber("/mavros/state", State, self.state_cb)
        rospy.Subscriber("/mavros/local_position/pose", PoseStamped, self.pose_cb)
        rospy.Subscriber("/mavros/local_position/velocity_local", TwistStamped, self.vel_cb)
        rospy.Subscriber("/gazebo/model_states", ModelStates, self.model_cb)

        self.vel_pub = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel', TwistStamped, queue_size=1)
        
        # Services
        self.arm_service = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool)
        self.mode_service = rospy.ServiceProxy('/mavros/set_mode', SetMode)

        self.search_t = 0.0
        self.origin_x = None
        self.origin_y = None
        
        self.rate = rospy.Rate(20)
        
        # State machine
        self.agent_state = "SEARCH"
        
        # Wait for MAVROS connection
        rospy.loginfo("Waiting for MAVROS connection...")
        while not rospy.is_shutdown() and not self.state.connected:
            self.rate.sleep()
        rospy.loginfo("MAVROS connected.")
        
    def state_cb(self, msg):
        self.state = msg

    def pose_cb(self, msg):
        self.pose = msg
        if self.origin_x is None:
            self.origin_x = msg.pose.position.x
            self.origin_y = msg.pose.position.y

    def vel_cb(self, msg):
        self.vel = msg

    def model_cb(self, msg):
        self.models = msg
        try:
            iris_idx = self.models.name.index("iris")
            pad_idx = self.models.name.index("aruco_pad")
            
            iris_pos = self.models.pose[iris_idx].position
            pad_pos = self.models.pose[pad_idx].position
            
            # Ground truth dx, dy in world frame
            # Transform to drone's downward camera view
            dx = pad_pos.x - iris_pos.x
            dy = pad_pos.y - iris_pos.y
            
            # Simulate detection cone (FOV limits)
            alt = max(0.1, iris_pos.z)
            dist_sq = dx**2 + dy**2
            max_dist = alt * math.tan(math.radians(45.0)) # 90 deg FOV
            
            if math.sqrt(dist_sq) < max_dist:
                self.target_detected = True
                self.target_dx = dx
                self.target_dy = dy
            else:
                self.target_detected = False
                
        except ValueError:
            self.target_detected = False

    # Tool 1: get_drone_state
    def get_drone_state(self):
        return {
            "alt": self.pose.pose.position.z,
            "vx": self.vel.twist.linear.x,
            "vy": self.vel.twist.linear.y,
            "vz": self.vel.twist.linear.z,
            "mode": self.state.mode,
            "armed": self.state.armed
        }

    # Tool 2: detect_visual_target
    def detect_visual_target(self):
        return self.target_detected, self.target_dx, self.target_dy

    # Tool 3: set_velocity
    def set_velocity(self, vx, vy, vz):
        # Guardrail: Mode & Armed Check
        if self.state.mode != "OFFBOARD" or not self.state.armed:
            rospy.logwarn_throttle(2, "Guardrail: Not in OFFBOARD or not ARMED!")
            return

        # Guardrail: Attitude/Speed limit to prevent "Roll failure"
        vx = max(-0.5, min(0.5, vx))
        vy = max(-0.5, min(0.5, vy))
        vz = max(-0.5, min(0.5, vz))

        cmd = TwistStamped()
        cmd.twist.linear.x = vx
        cmd.twist.linear.y = vy
        cmd.twist.linear.z = vz
        self.vel_pub.publish(cmd)

    # Tool 4: land_and_disarm
    def land_and_disarm(self):
        rospy.loginfo("Executing FINAL LANDING.")
        self.mode_service(custom_mode="AUTO.LAND")
        while not rospy.is_shutdown() and self.pose.pose.position.z > 0.1:
            rospy.loginfo_throttle(1, f"Landing... Alt: {self.pose.pose.position.z:.2f}m")
            self.rate.sleep()
        
        rospy.loginfo("Disarming...")
        self.arm_service(False)
        self.agent_state = "DONE"
        
    def check_guardrails(self):
        if self.origin_x is None: return True
        
        # 1. Boundary check: > 10m
        dist_origin = math.hypot(self.pose.pose.position.x - self.origin_x, 
                                 self.pose.pose.position.y - self.origin_y)
        if dist_origin > 10.0 and self.state.mode == "OFFBOARD":
            rospy.logerr("Guardrail limit exceeded: Distance > 10m! Switching to AUTO.RTL")
            self.mode_service(custom_mode="AUTO.RTL")
            return False
            
        # 2. Heading stable check (simulated with yaw rate)
        yaw_rate = abs(self.vel.twist.angular.z)
        if yaw_rate > 1.0: # ~60 deg/s
            rospy.logwarn("Guardrail: Heading estimate not stable. Hovering.")
            if self.state.mode == "OFFBOARD":
                cmd = TwistStamped()
                self.vel_pub.publish(cmd) # hover
            return False
            
        return True

    def run(self):
        # Wait for a bit
        for i in range(100):
            cmd = TwistStamped()
            self.vel_pub.publish(cmd)
            self.rate.sleep()
            
        # Takeoff Sequence
        if self.state.mode != "OFFBOARD":
            self.mode_service(custom_mode="OFFBOARD")
            self.arm_service(True)
            
        rospy.loginfo("Starting Agent Logic Loop.")
        
        while not rospy.is_shutdown():
            if self.agent_state == "DONE":
                break
                
            if not self.check_guardrails():
                self.rate.sleep()
                continue
                
            state_dict = self.get_drone_state()
            detected, dx, dy = self.detect_visual_target()
            alt = state_dict["alt"]
            
            if self.agent_state == "SEARCH":
                if detected:
                    rospy.loginfo("Target Detected! Switching to TRACKING.")
                    self.agent_state = "TRACKING"
                else:
                    # Ascend to 2.5m and do Z-pattern
                    vz = 0.5 if alt < 2.4 else (-0.5 if alt > 2.6 else 0.0)
                    vx = 0.4 * math.sin(self.search_t)
                    vy = -0.4 if math.cos(self.search_t) > 0 else 0.4
                    self.set_velocity(vx, vy, vz)
                    self.search_t += 0.05
                    rospy.loginfo_throttle(2, "SEARCH: Executing Z-pattern at ~2.5m")

            elif self.agent_state == "TRACKING":
                if not detected:
                    rospy.logwarn("Target Lost! Back to SEARCH.")
                    self.agent_state = "SEARCH"
                    continue
                
                dist = math.hypot(dx, dy)
                if dist < 0.2:
                    rospy.loginfo("Aligned! Switching to ALIGN_DESCEND.")
                    self.agent_state = "ALIGN_DESCEND"
                else:
                    # PD control placeholder (predictive)
                    vx = dx * 1.0
                    vy = dy * 1.0
                    vz = 0.5 if alt < 2.4 else (-0.5 if alt > 2.6 else 0.0)
                    self.set_velocity(vx, vy, vz)
                    rospy.loginfo_throttle(1, f"TRACKING: Error dx={dx:.2f}, dy={dy:.2f}")

            elif self.agent_state == "ALIGN_DESCEND":
                if not detected:
                    rospy.logwarn("Target Lost! Back to SEARCH.")
                    self.agent_state = "SEARCH"
                    continue
                
                dist = math.hypot(dx, dy)
                total_v = math.hypot(state_dict["vx"], state_dict["vy"])
                
                if alt < 0.3 and total_v < 0.2:
                    self.agent_state = "FINAL_LANDING"
                else:
                    # Maintain XY alignment while descending
                    vx = dx * 1.5
                    vy = dy * 1.5
                    vz = -0.3 # Slow descend
                    self.set_velocity(vx, vy, vz)
                    rospy.loginfo_throttle(1, f"ALIGN_DESCEND: Alt={alt:.2f}m, Error={dist:.2f}m")

            elif self.agent_state == "FINAL_LANDING":
                self.land_and_disarm()

            self.rate.sleep()

if __name__ == '__main__':
    try:
        agent = IrisAgent()
        agent.run()
    except rospy.ROSInterruptException:
        pass
