#!/bin/bash

# 0. Clean up PX4 EEPROM from previous runs to prevent corruption
rm -f ~/.ros/eeprom/parameters*

# 1. Source catkin workspace
source /opt/ros/noetic/setup.bash
source /root/ros_ws/devel/setup.bash

# 2. Setup PX4 environment
source /root/ros_ws/PX4-Autopilot/Tools/setup_gazebo.bash /root/ros_ws/PX4-Autopilot /root/ros_ws/PX4-Autopilot/build/px4_sitl_default

# 3. Explicitly export PX4 and XTDrone ROS_PACKAGE_PATHs which get wiped by catkin's setup.bash
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:/root/ros_ws/PX4-Autopilot:/root/ros_ws/PX4-Autopilot/Tools/sitl_gazebo:/root/XTDrone/sitl_config
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:/root/XTDrone/sitl_config/models:/root/ros_ws/src/rl_drone_yolo/models

# 4. MODERATE SPEED MODE
# 10x was too fast for some EKF convergences. Reducing to 5x for better stability.
export PX4_SIM_SPEED_FACTOR=5

# 5. Launch the simulation
echo "Starting 5X Accelerated RL simulation environment..."
roslaunch rl_drone_yolo rl_sim.launch
