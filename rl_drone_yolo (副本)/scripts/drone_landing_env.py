#!/usr/bin/env python3
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import os
import rospy
import time
import math
from geometry_msgs.msg import TwistStamped, PoseStamped
from mavros_msgs.msg import State
from mavros_msgs.srv import CommandBool, SetMode
from gazebo_msgs.msg import ModelStates, ModelState
from gazebo_msgs.srv import SetModelState
from geometry_msgs.msg import Point
import gymnasium as gym

class DroneLandingEnv(gym.Env):
    """
    ROS-based Gym Environment for PX4 UAV landing on a moving pad.
    """
    metadata = {'render.modes': ['console']}

    def __init__(self, drone_id=0, is_multiagent=False):
        super(DroneLandingEnv, self).__init__()
        
        self.drone_id = drone_id
        self.is_multiagent = is_multiagent
        
        if self.is_multiagent:
            self.vehicle_name = f"iris{drone_id}" # Spawned by single_vehicle_spawn
            self.pad_name = f"aruco_pad_{drone_id}"
            self.ns = f"/iris_{drone_id}"
        else:
            self.vehicle_name = "iris"
            self.pad_name = "aruco_pad"
            self.ns = ""
        
        # Initialize ROS node (only once)
        try:
            rospy.init_node(f'rl_drone_env_{drone_id}', anonymous=True)
            rospy.loginfo(f"Initialized Gym RL ROS Node for Drone {drone_id}")
        except rospy.ROSException:
            pass # Node already initialized
            
        # Action space: [vx, vy, vz] mapped to [-1, 1], representing max [-0.5, 0.5] m/s
        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(3,), dtype=np.float32)
        
        # Observation space: [dx, dy, dz, vx_body, vy_body, prev_ax, prev_ay, prev_az] in body frame
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(8,), dtype=np.float32)

        # States
        self.state_msg = State()
        self.pose = PoseStamped()
        self.vel = TwistStamped()
        
        self.iris_pos = None
        self.pad_pos = None
        self.current_yaw = 0.0
        
        # ROS pub/sub with namespaces
        rospy.Subscriber(f"{self.ns}/mavros/state", State, self.state_cb)
        rospy.Subscriber(f"{self.ns}/mavros/local_position/pose", PoseStamped, self.pose_cb)
        rospy.Subscriber(f"{self.ns}/mavros/local_position/velocity_local", TwistStamped, self.vel_cb)
        rospy.Subscriber("/gazebo/model_states", ModelStates, self.model_cb)
        rospy.Subscriber("/rl_drone/yolo/detection", Point, self.yolo_cb)
        
        self.yolo_pos = None
        self.last_yolo_time = 0.0
        
        self.vel_pub = rospy.Publisher(f'{self.ns}/mavros/setpoint_velocity/cmd_vel', TwistStamped, queue_size=1)
        
        # ROS Services
        self.arm_service = rospy.ServiceProxy(f'{self.ns}/mavros/cmd/arming', CommandBool)
        self.mode_service = rospy.ServiceProxy(f'{self.ns}/mavros/set_mode', SetMode)
        self.set_model_state_service = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
        
        self.rate = rospy.Rate(10) # 10Hz control loop for RL
        self.max_steps = 400
        self.current_step = 0
        self.prev_action = np.zeros(3, dtype=np.float32)
        self.search_t = 0.0
        
    def state_cb(self, msg): self.state_msg = msg
    def vel_cb(self, msg): self.vel = msg
    
    def pose_cb(self, msg):
        self.pose = msg
        q = msg.pose.orientation
        siny_cosp = 2 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
        self.current_yaw = math.atan2(siny_cosp, cosy_cosp)
        
        # Calculate pitch
        sinp = 2 * (q.w * q.y - q.z * q.x)
        if abs(sinp) >= 1:
            self.current_pitch = math.copysign(math.pi / 2, sinp)
        else:
            self.current_pitch = math.asin(sinp)
            
        # Calculate roll
        sinr_cosp = 2 * (q.w * q.x + q.y * q.z)
        cosr_cosp = 1 - 2 * (q.x * q.x + q.y * q.y)
        self.current_roll = math.atan2(sinr_cosp, cosr_cosp)
        
    def yolo_cb(self, msg):
        self.yolo_pos = msg
        self.last_yolo_time = time.time()

    def model_cb(self, msg):
        try:
            iris_idx = msg.name.index(self.vehicle_name)
            # pad_idx = msg.name.index(self.pad_name) # No longer using directly for obs
            self.iris_pos = msg.pose[iris_idx].position
            # For logging/evaluation purposes, we might still want to know pad position
            try:
                pad_idx = msg.name.index(self.pad_name)
                self.pad_pos = msg.pose[pad_idx].position
            except ValueError:
                pass
        except ValueError:
            pass

    def wait_for_connection(self):
        # Use python time in case ROS simulator clock is dead
        timeout_start = time.time()
        while not rospy.is_shutdown() and not self.state_msg.connected:
            if time.time() - timeout_start > 30.0:
                rospy.logerr("RL Timeout: Failed to connect to PX4/Mavros within 30 seconds.")
                raise Exception("PX4_CONNECTION_TIMEOUT")
            self.rate.sleep()

    def set_drone_mode(self, mode):
        # send setpoints
        for _ in range(10):
            cmd = TwistStamped()
            cmd.header.stamp = rospy.Time.now()
            self.vel_pub.publish(cmd)
            self.rate.sleep()
        self.mode_service(custom_mode=mode)
        
    def reset(self, seed=None, options=None):
        if seed is not None:
            np.random.seed(seed)
        self.current_step = 0
        self.prev_action = np.zeros(3, dtype=np.float32)
        self.wait_for_connection()
        
        # Wait for Gazebo node list to initialize before retrieving position
        if self.iris_pos is None or self.pad_pos is None:
            rospy.loginfo("Waiting for Gazebo models to load before resetting...")
            while (self.iris_pos is None or self.pad_pos is None) and not rospy.is_shutdown():
                self.rate.sleep()
                
        # Determine physical origin offset for multi-agent segregation
        base_y = self.drone_id * 20.0 if self.is_multiagent else 0.0
        
        # Ensure drone is upright, in bounds, and recovers
        flip = abs(getattr(self, 'current_roll', 0.0)) > 1.2 or abs(getattr(self, 'current_pitch', 0.0)) > 1.2
        dist_base = math.hypot(self.pose.pose.position.x, self.pose.pose.position.y - base_y)
        out_of_bounds = dist_base > 12.0
        
        if flip:
            rospy.logerr(f"RL Reset [{self.drone_id}]: Drone flipped! PX4 EKF crash lockdown is unrecoverable via teleport. Forcing hard environment reboot...")
            raise Exception("DRONE_FLIPPED_UNRECOVERABLE")
            
        if out_of_bounds or self.pose.pose.position.z < 0.2:
            if out_of_bounds:
                rospy.logwarn(f"RL Reset [{self.drone_id}]: Drone OOB. Forcing teleport to recover...")
                
                # 1. Disarm to ensure safety and reset PX4 state machine
                try:
                    self.arm_service(False)
                except Exception:
                    pass
                    
                iris_state = ModelState()
                iris_state.model_name = self.vehicle_name
                # Teleport drone to a fixed starting location near its cell base
                iris_state.pose.position.x = 0.0
                iris_state.pose.position.y = base_y - 8.0
                iris_state.pose.position.z = 1.0
                iris_state.pose.orientation.w = 1.0
                # Halt all physics velocity to prevent drift post-teleport
                iris_state.twist.linear.x = 0.0
                iris_state.twist.linear.y = 0.0
                iris_state.twist.linear.z = 0.0
                iris_state.twist.angular.x = 0.0
                iris_state.twist.angular.y = 0.0
                iris_state.twist.angular.z = 0.0
                self.set_model_state_service(iris_state)
                
                # 2. Wait for EKF to calm down after teleport jump.
                # Increase wait to 8 seconds and ensure we are in a known state
                rospy.loginfo("Streaming 0-velocity for 8s to let EKF converge after jump...")
                for _ in range(80):
                    cmd = TwistStamped()
                    cmd.header.stamp = rospy.Time.now()
                    self.vel_pub.publish(cmd)
                    self.rate.sleep()
            rospy.loginfo("RL Reset: Taking off via OFFBOARD Velocity control to 5.0m...")
            takeoff_start = time.time()
            
            while not rospy.is_shutdown() and self.pose.pose.position.z < 5.0:
                # Use OFFBOARD to brute-force lift the drone instead of AUTO.TAKEOFF
                # Send upward velocity
                cmd = TwistStamped()
                cmd.header.stamp = rospy.Time.now()
                cmd.twist.linear.x = 0.0
                cmd.twist.linear.y = 0.0
                cmd.twist.linear.z = 1.0  # 1 m/s up
                self.vel_pub.publish(cmd)
                
                try:
                    if self.state_msg.mode != "OFFBOARD":
                        self.mode_service(custom_mode="OFFBOARD")
                    if not self.state_msg.armed:
                        self.arm_service(True)
                except Exception:
                    pass
                    
                if time.time() - takeoff_start > 60.0:
                    rospy.logwarn("Takeoff timeout! Drone might be stuck computing ACC offsets or EKF divergence.")
                    raise Exception("PX4_TAKEOFF_TIMEOUT")
                self.rate.sleep()

        # 1. Teleport the target pad to a random location in world coordinates
        # using the multi-agent segregated base
        base_y = self.drone_id * 20.0 if self.is_multiagent else 0.0
        new_pad_x = np.random.uniform(-5.0, 5.0)
        new_pad_y = base_y + np.random.uniform(-5.0, 5.0)
        
        state_msg = ModelState()
        state_msg.model_name = self.pad_name
        state_msg.pose.position.x = new_pad_x
        state_msg.pose.position.y = new_pad_y
        state_msg.pose.position.z = 0.0
        self.set_model_state_service(state_msg)
            
        # 2. Command hover at 5.0m offset
        rospy.loginfo("RL Reset: Climbing to 5.0m hover...")
        target_z = 5.0
        stable_count = 0
        timeout_start = time.time()
        
        # Continuously enforce OFFBOARD and arming in the hover loop as well
        while not rospy.is_shutdown() and stable_count < 10:
            if time.time() - timeout_start > 10.0:
                rospy.logwarn("Hover timeout! Skipping wait.")
                break
                
            if self.state_msg.mode != "OFFBOARD":
                self.mode_service(custom_mode="OFFBOARD")
            if not self.state_msg.armed:
                self.arm_service(True)
                
            dz = target_z - self.pose.pose.position.z
            cmd = TwistStamped()
            cmd.header.stamp = rospy.Time.now()
            # P control for Z
            cmd.twist.linear.z = max(-0.5, min(0.5, dz * 1.0))
            cmd.twist.linear.x = 0.0
            cmd.twist.linear.y = 0.0
            self.vel_pub.publish(cmd)
            
            if abs(dz) < 0.2:
                stable_count += 1
            else:
                stable_count = 0
                
            self.rate.sleep()
            
        # 3. Wait until YOLO detects the target before starting
        rospy.loginfo("RL Reset: Searching for target platform...")
        self.search_t = 0.0
        while not rospy.is_shutdown() and (self.yolo_pos is None or (time.time() - self.last_yolo_time) > 1.0):
            self.search_t += 0.1
            dist_to_origin = math.hypot(self.pose.pose.position.x, self.pose.pose.position.y)
            v_max = 0.5
            
            cmd = TwistStamped()
            cmd.header.stamp = rospy.Time.now()
            
            if dist_to_origin > 2.0:
                # Fly to origin
                angle_to_origin = math.atan2(-self.pose.pose.position.y, -self.pose.pose.position.x)
                cmd.twist.linear.x = v_max * math.cos(angle_to_origin)
                cmd.twist.linear.y = v_max * math.sin(angle_to_origin)
            else:
                # Expanding circle search
                r = 0.5 + 0.02 * self.search_t
                omega = 0.5
                cmd.twist.linear.x = -r * omega * math.sin(omega * self.search_t)
                cmd.twist.linear.y = r * omega * math.cos(omega * self.search_t)
                
            cmd.twist.linear.z = (5.0 - self.pose.pose.position.z) * 0.5
            self.vel_pub.publish(cmd)
            self.rate.sleep()
            
        rospy.loginfo("RL Reset complete. Target detected.")
        # Compatible with gym 0.26 return type (obs, info)
        obs = self._get_obs()
        self.prev_potential = math.hypot(obs[0], obs[1]) + 1.5 * obs[2]
        return obs, {}

    def _get_obs(self):
        if self.iris_pos is None:
            return np.zeros(8, dtype=np.float32)
            
        # Try to use YOLO detection
        if self.yolo_pos is not None and (time.time() - self.last_yolo_time) < 0.5:
            # Reconstruct dx_b, dy_b from YOLO normalized coordinates
            # nx, ny are in [-1, 1]. For monocular_camera with FOV=120 deg
            # Camera orientation: looking down (pitch=pi/2).
            # nx -> -dy_b, ny -> -dx_b
            z = self.iris_pos.z
            # fpv_cam FOV is ~60 deg (1.047 rad). tan(fov/2) = tan(30 deg) = 0.577
            dx_b = -self.yolo_pos.y * z * 0.577 
            dy_b = -self.yolo_pos.x * z * 0.577
            dz = max(0.0, self.iris_pos.z) # Assume pad is at z=0
        else:
            # If no detection, use a large error or last known position (here we use 0 observation but with large distance)
            dx_b = 0.0
            dy_b = 0.0
            dz = max(0.0, self.iris_pos.z)
            # Or we could just fallback to pad_pos for training (but user asked to change source)
            # Let's use 0 for now which might confuse the agent if it thinks it's already there.
            # A better approach would be to include a "detected" flag in observation.
            # But the observation space is fixed at 8.
            # Maybe use large values to indicate "not found"?
            dx_b = 10.0 
            dy_b = 10.0
        
        vx_b = self.vel.twist.linear.x
        vy_b = self.vel.twist.linear.y
        
        return np.array([dx_b, dy_b, dz, vx_b, vy_b, 
                         self.prev_action[0], self.prev_action[1], self.prev_action[2]], dtype=np.float32)

    def step(self, action):
        self.current_step += 1
        
        # Execute search behavior if target is lost
        if self.yolo_pos is None or (time.time() - self.last_yolo_time) > 1.0:
            self.search_t += 0.1
            # 1. Fly to origin (0,0) first
            dist_to_origin = math.hypot(self.pose.pose.position.x, self.pose.pose.position.y)
            v_max = 0.5
            
            cmd = TwistStamped()
            cmd.header.stamp = rospy.Time.now()
            
            if dist_to_origin > 2.0:
                # Direct flight to origin
                angle_to_origin = math.atan2(-self.pose.pose.position.y, -self.pose.pose.position.x)
                cmd.twist.linear.x = v_max * math.cos(angle_to_origin)
                cmd.twist.linear.y = v_max * math.sin(angle_to_origin)
                rospy.loginfo_throttle(5, "Target Lost: Flying back to origin...")
            else:
                # Close to origin, perform expanding circle search
                # Radius grows slowly: r = 0.5 + 0.1*t
                r = 0.5 + 0.02 * self.search_t
                omega = 0.5 # rad/s
                search_vx = -r * omega * math.sin(omega * self.search_t)
                search_vy = r * omega * math.cos(omega * self.search_t)
                cmd.twist.linear.x = search_vx
                cmd.twist.linear.y = search_vy
                rospy.loginfo_throttle(5, f"Target Lost: Expanding circle search (r={r:.2f}m)...")
                
            cmd.twist.linear.z = (5.0 - self.pose.pose.position.z) * 0.5
            self.vel_pub.publish(cmd)
        else:
            # Normal RL control
            self.search_t = 0.0
            # map action [-1, 1] to velocity [-0.5, 0.5]
            vx = float(action[0]) * 0.5
            vy = float(action[1]) * 0.5
            vz = float(action[2]) * 0.5
            
            cmd = TwistStamped()
            cmd.header.stamp = rospy.Time.now()
            cmd.twist.linear.x = vx
            cmd.twist.linear.y = vy
            cmd.twist.linear.z = vz
            self.vel_pub.publish(cmd)
        
        # Enforce 10Hz step rate
        self.rate.sleep()
        
        obs = self._get_obs()
        dx_b, dy_b, dz, vx_body, vy_body, _, _, _ = obs
        
        dist_xy = math.hypot(dx_b, dy_b)
        dist_3d = math.sqrt(dx_b**2 + dy_b**2 + dz**2)
        
        # 1. Delta Distance Potential-based shaping (Guaranteed no-farming)
        # We value z-distance (altitude) slightly more to encourage descending
        current_potential = math.hypot(dx_b, dy_b) + 1.5 * dz
        if not hasattr(self, 'prev_potential'):
            self.prev_potential = current_potential
            
        delta_potential = self.prev_potential - current_potential
        self.prev_potential = current_potential
        
        # Reward for moving closer to the target zone
        reward = delta_potential * 100.0 
        
        # 2. Continuous Distance Reward Shaping
        # Give constant positive reinforcement for staying near the target
        reward += max(0, 2.0 - dist_3d) * 2.0
        
        # 3. Time/Hover Bleeding Penalty 
        # Forces the drone to end the episode as fast as possible instead of hovering
        reward -= 0.5
        
        # 4. Action Smoothing (Jerk) Penalty to stop oscillation
        jerk = np.sum(np.abs(np.array(action) - self.prev_action))
        reward -= 0.02 * jerk
        self.prev_action = np.array(action, dtype=np.float32)
        
        terminated = False
        truncated = False
        info = {}
        
        # Termination conditions
        flip = abs(getattr(self, 'current_roll', 0.0)) > 1.2 or abs(getattr(self, 'current_pitch', 0.0)) > 1.2
        if flip:
            # Flipped over
            reward -= 100.0
            terminated = True
            info['is_success'] = False
            rospy.logwarn("RL Episode: Crash! Drone flipped over.")
            
        elif dist_xy < 0.4 and dz < 0.3:
            # Success! widened radius to 0.5m (1m diameter)
            reward += 1000.0  # Mega Bonus for achieving the ultimate goal
            terminated = True
            info['is_success'] = True
            rospy.loginfo("RL Episode: Success! Hit the target.")
            
        elif dist_xy > 15.0:
            # Out of bounds
            reward -= 100.0
            terminated = True
            info['is_success'] = False
            rospy.loginfo(f"RL Episode: Terminated OOB. dist_xy={dist_xy:.2f}, pad=({self.pad_pos.x:.2f},{self.pad_pos.y:.2f}), drone=({self.iris_pos.x:.2f},{self.iris_pos.y:.2f})")
            
        elif dz < 0.1 and dist_xy > 0.4:
            # Ground crash
            reward -= 100.0
            terminated = True
            info['is_success'] = False
            rospy.loginfo("RL Episode: Ground crash missed target.")
            
        if self.current_step >= self.max_steps:
            # Timeout
            truncated = True
            info['is_success'] = False
            rospy.loginfo("RL Episode: Truncated due to timeout.")
            
        # Compatible with gym 0.26 return type (obs, reward, terminated, truncated, info)
        return obs, reward, terminated, truncated, info

