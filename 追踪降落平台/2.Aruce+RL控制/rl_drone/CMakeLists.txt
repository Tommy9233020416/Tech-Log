cmake_minimum_required(VERSION 3.0.2)
project(rl_drone)

find_package(catkin REQUIRED COMPONENTS
  rospy
  geometry_msgs
  mavros_msgs
  gazebo_msgs
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES rl_drone
#  CATKIN_DEPENDS rospy
#  DEPENDS system_lib
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

catkin_install_python(PROGRAMS
  scripts/target_mover.py
  scripts/iris_agent.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
