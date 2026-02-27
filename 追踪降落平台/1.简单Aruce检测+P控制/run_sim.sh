#!/bin/bash

# 1. Source catkin workspace
source /opt/ros/noetic/setup.bash
source /root/catkin_ws/devel/setup.bash

# 2. Setup PX4 environment
source /root/PX4-Autopilot/Tools/setup_gazebo.bash /root/PX4-Autopilot /root/PX4-Autopilot/build/px4_sitl_default

# 3. Explicitly export PX4 and XTDrone ROS_PACKAGE_PATHs which get wiped by catkin's setup.bash
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:/root/PX4-Autopilot:/root/PX4-Autopilot/Tools/sitl_gazebo:/root/XTDrone/sitl_config
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:/root/XTDrone/sitl_config/models:/root/catkin_ws/src/rl_drone/models

# 4. Launch the simulation
echo "Starting simulation..."
roslaunch rl_drone agent_sim.launch
