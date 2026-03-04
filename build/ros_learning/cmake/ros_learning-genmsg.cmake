# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "ros_learning: 7 messages, 0 services")

set(MSG_I_FLAGS "-Iros_learning:/root/catkin_ws/devel/share/ros_learning/msg;-Igeometry_msgs:/opt/ros/noetic/share/geometry_msgs/cmake/../msg;-Istd_msgs:/opt/ros/noetic/share/std_msgs/cmake/../msg;-Iactionlib_msgs:/opt/ros/noetic/share/actionlib_msgs/cmake/../msg;-Imavros_msgs:/opt/ros/noetic/share/mavros_msgs/cmake/../msg;-Igeographic_msgs:/opt/ros/noetic/share/geographic_msgs/cmake/../msg;-Isensor_msgs:/opt/ros/noetic/share/sensor_msgs/cmake/../msg;-Iuuid_msgs:/opt/ros/noetic/share/uuid_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(ros_learning_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingAction.msg" NAME_WE)
add_custom_target(_ros_learning_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "ros_learning" "/root/catkin_ws/devel/share/ros_learning/msg/LandingAction.msg" "ros_learning/LandingActionGoal:ros_learning/LandingFeedback:actionlib_msgs/GoalID:std_msgs/Header:ros_learning/LandingActionResult:ros_learning/LandingGoal:ros_learning/LandingActionFeedback:actionlib_msgs/GoalStatus:ros_learning/LandingResult"
)

get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionGoal.msg" NAME_WE)
add_custom_target(_ros_learning_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "ros_learning" "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionGoal.msg" "std_msgs/Header:ros_learning/LandingGoal:actionlib_msgs/GoalID"
)

get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionResult.msg" NAME_WE)
add_custom_target(_ros_learning_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "ros_learning" "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionResult.msg" "std_msgs/Header:actionlib_msgs/GoalStatus:actionlib_msgs/GoalID:ros_learning/LandingResult"
)

get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionFeedback.msg" NAME_WE)
add_custom_target(_ros_learning_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "ros_learning" "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionFeedback.msg" "ros_learning/LandingFeedback:std_msgs/Header:actionlib_msgs/GoalStatus:actionlib_msgs/GoalID"
)

get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingGoal.msg" NAME_WE)
add_custom_target(_ros_learning_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "ros_learning" "/root/catkin_ws/devel/share/ros_learning/msg/LandingGoal.msg" ""
)

get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingResult.msg" NAME_WE)
add_custom_target(_ros_learning_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "ros_learning" "/root/catkin_ws/devel/share/ros_learning/msg/LandingResult.msg" ""
)

get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingFeedback.msg" NAME_WE)
add_custom_target(_ros_learning_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "ros_learning" "/root/catkin_ws/devel/share/ros_learning/msg/LandingFeedback.msg" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(ros_learning
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingAction.msg"
  "${MSG_I_FLAGS}"
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionGoal.msg;/root/catkin_ws/devel/share/ros_learning/msg/LandingFeedback.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/root/catkin_ws/devel/share/ros_learning/msg/LandingActionResult.msg;/root/catkin_ws/devel/share/ros_learning/msg/LandingGoal.msg;/root/catkin_ws/devel/share/ros_learning/msg/LandingActionFeedback.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/root/catkin_ws/devel/share/ros_learning/msg/LandingResult.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ros_learning
)
_generate_msg_cpp(ros_learning
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/root/catkin_ws/devel/share/ros_learning/msg/LandingGoal.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ros_learning
)
_generate_msg_cpp(ros_learning
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/root/catkin_ws/devel/share/ros_learning/msg/LandingResult.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ros_learning
)
_generate_msg_cpp(ros_learning
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingFeedback.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ros_learning
)
_generate_msg_cpp(ros_learning
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingGoal.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ros_learning
)
_generate_msg_cpp(ros_learning
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingResult.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ros_learning
)
_generate_msg_cpp(ros_learning
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingFeedback.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ros_learning
)

### Generating Services

### Generating Module File
_generate_module_cpp(ros_learning
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ros_learning
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(ros_learning_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(ros_learning_generate_messages ros_learning_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingAction.msg" NAME_WE)
add_dependencies(ros_learning_generate_messages_cpp _ros_learning_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionGoal.msg" NAME_WE)
add_dependencies(ros_learning_generate_messages_cpp _ros_learning_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionResult.msg" NAME_WE)
add_dependencies(ros_learning_generate_messages_cpp _ros_learning_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionFeedback.msg" NAME_WE)
add_dependencies(ros_learning_generate_messages_cpp _ros_learning_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingGoal.msg" NAME_WE)
add_dependencies(ros_learning_generate_messages_cpp _ros_learning_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingResult.msg" NAME_WE)
add_dependencies(ros_learning_generate_messages_cpp _ros_learning_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingFeedback.msg" NAME_WE)
add_dependencies(ros_learning_generate_messages_cpp _ros_learning_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(ros_learning_gencpp)
add_dependencies(ros_learning_gencpp ros_learning_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS ros_learning_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(ros_learning
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingAction.msg"
  "${MSG_I_FLAGS}"
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionGoal.msg;/root/catkin_ws/devel/share/ros_learning/msg/LandingFeedback.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/root/catkin_ws/devel/share/ros_learning/msg/LandingActionResult.msg;/root/catkin_ws/devel/share/ros_learning/msg/LandingGoal.msg;/root/catkin_ws/devel/share/ros_learning/msg/LandingActionFeedback.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/root/catkin_ws/devel/share/ros_learning/msg/LandingResult.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/ros_learning
)
_generate_msg_eus(ros_learning
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/root/catkin_ws/devel/share/ros_learning/msg/LandingGoal.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/ros_learning
)
_generate_msg_eus(ros_learning
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/root/catkin_ws/devel/share/ros_learning/msg/LandingResult.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/ros_learning
)
_generate_msg_eus(ros_learning
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingFeedback.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/ros_learning
)
_generate_msg_eus(ros_learning
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingGoal.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/ros_learning
)
_generate_msg_eus(ros_learning
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingResult.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/ros_learning
)
_generate_msg_eus(ros_learning
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingFeedback.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/ros_learning
)

### Generating Services

### Generating Module File
_generate_module_eus(ros_learning
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/ros_learning
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(ros_learning_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(ros_learning_generate_messages ros_learning_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingAction.msg" NAME_WE)
add_dependencies(ros_learning_generate_messages_eus _ros_learning_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionGoal.msg" NAME_WE)
add_dependencies(ros_learning_generate_messages_eus _ros_learning_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionResult.msg" NAME_WE)
add_dependencies(ros_learning_generate_messages_eus _ros_learning_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionFeedback.msg" NAME_WE)
add_dependencies(ros_learning_generate_messages_eus _ros_learning_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingGoal.msg" NAME_WE)
add_dependencies(ros_learning_generate_messages_eus _ros_learning_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingResult.msg" NAME_WE)
add_dependencies(ros_learning_generate_messages_eus _ros_learning_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingFeedback.msg" NAME_WE)
add_dependencies(ros_learning_generate_messages_eus _ros_learning_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(ros_learning_geneus)
add_dependencies(ros_learning_geneus ros_learning_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS ros_learning_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(ros_learning
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingAction.msg"
  "${MSG_I_FLAGS}"
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionGoal.msg;/root/catkin_ws/devel/share/ros_learning/msg/LandingFeedback.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/root/catkin_ws/devel/share/ros_learning/msg/LandingActionResult.msg;/root/catkin_ws/devel/share/ros_learning/msg/LandingGoal.msg;/root/catkin_ws/devel/share/ros_learning/msg/LandingActionFeedback.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/root/catkin_ws/devel/share/ros_learning/msg/LandingResult.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ros_learning
)
_generate_msg_lisp(ros_learning
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/root/catkin_ws/devel/share/ros_learning/msg/LandingGoal.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ros_learning
)
_generate_msg_lisp(ros_learning
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/root/catkin_ws/devel/share/ros_learning/msg/LandingResult.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ros_learning
)
_generate_msg_lisp(ros_learning
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingFeedback.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ros_learning
)
_generate_msg_lisp(ros_learning
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingGoal.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ros_learning
)
_generate_msg_lisp(ros_learning
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingResult.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ros_learning
)
_generate_msg_lisp(ros_learning
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingFeedback.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ros_learning
)

### Generating Services

### Generating Module File
_generate_module_lisp(ros_learning
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ros_learning
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(ros_learning_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(ros_learning_generate_messages ros_learning_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingAction.msg" NAME_WE)
add_dependencies(ros_learning_generate_messages_lisp _ros_learning_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionGoal.msg" NAME_WE)
add_dependencies(ros_learning_generate_messages_lisp _ros_learning_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionResult.msg" NAME_WE)
add_dependencies(ros_learning_generate_messages_lisp _ros_learning_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionFeedback.msg" NAME_WE)
add_dependencies(ros_learning_generate_messages_lisp _ros_learning_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingGoal.msg" NAME_WE)
add_dependencies(ros_learning_generate_messages_lisp _ros_learning_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingResult.msg" NAME_WE)
add_dependencies(ros_learning_generate_messages_lisp _ros_learning_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingFeedback.msg" NAME_WE)
add_dependencies(ros_learning_generate_messages_lisp _ros_learning_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(ros_learning_genlisp)
add_dependencies(ros_learning_genlisp ros_learning_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS ros_learning_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(ros_learning
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingAction.msg"
  "${MSG_I_FLAGS}"
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionGoal.msg;/root/catkin_ws/devel/share/ros_learning/msg/LandingFeedback.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/root/catkin_ws/devel/share/ros_learning/msg/LandingActionResult.msg;/root/catkin_ws/devel/share/ros_learning/msg/LandingGoal.msg;/root/catkin_ws/devel/share/ros_learning/msg/LandingActionFeedback.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/root/catkin_ws/devel/share/ros_learning/msg/LandingResult.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/ros_learning
)
_generate_msg_nodejs(ros_learning
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/root/catkin_ws/devel/share/ros_learning/msg/LandingGoal.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/ros_learning
)
_generate_msg_nodejs(ros_learning
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/root/catkin_ws/devel/share/ros_learning/msg/LandingResult.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/ros_learning
)
_generate_msg_nodejs(ros_learning
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingFeedback.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/ros_learning
)
_generate_msg_nodejs(ros_learning
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingGoal.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/ros_learning
)
_generate_msg_nodejs(ros_learning
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingResult.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/ros_learning
)
_generate_msg_nodejs(ros_learning
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingFeedback.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/ros_learning
)

### Generating Services

### Generating Module File
_generate_module_nodejs(ros_learning
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/ros_learning
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(ros_learning_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(ros_learning_generate_messages ros_learning_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingAction.msg" NAME_WE)
add_dependencies(ros_learning_generate_messages_nodejs _ros_learning_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionGoal.msg" NAME_WE)
add_dependencies(ros_learning_generate_messages_nodejs _ros_learning_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionResult.msg" NAME_WE)
add_dependencies(ros_learning_generate_messages_nodejs _ros_learning_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionFeedback.msg" NAME_WE)
add_dependencies(ros_learning_generate_messages_nodejs _ros_learning_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingGoal.msg" NAME_WE)
add_dependencies(ros_learning_generate_messages_nodejs _ros_learning_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingResult.msg" NAME_WE)
add_dependencies(ros_learning_generate_messages_nodejs _ros_learning_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingFeedback.msg" NAME_WE)
add_dependencies(ros_learning_generate_messages_nodejs _ros_learning_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(ros_learning_gennodejs)
add_dependencies(ros_learning_gennodejs ros_learning_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS ros_learning_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(ros_learning
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingAction.msg"
  "${MSG_I_FLAGS}"
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionGoal.msg;/root/catkin_ws/devel/share/ros_learning/msg/LandingFeedback.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/root/catkin_ws/devel/share/ros_learning/msg/LandingActionResult.msg;/root/catkin_ws/devel/share/ros_learning/msg/LandingGoal.msg;/root/catkin_ws/devel/share/ros_learning/msg/LandingActionFeedback.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/root/catkin_ws/devel/share/ros_learning/msg/LandingResult.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ros_learning
)
_generate_msg_py(ros_learning
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/root/catkin_ws/devel/share/ros_learning/msg/LandingGoal.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ros_learning
)
_generate_msg_py(ros_learning
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/root/catkin_ws/devel/share/ros_learning/msg/LandingResult.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ros_learning
)
_generate_msg_py(ros_learning
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingFeedback.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/noetic/share/actionlib_msgs/cmake/../msg/GoalID.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ros_learning
)
_generate_msg_py(ros_learning
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingGoal.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ros_learning
)
_generate_msg_py(ros_learning
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingResult.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ros_learning
)
_generate_msg_py(ros_learning
  "/root/catkin_ws/devel/share/ros_learning/msg/LandingFeedback.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ros_learning
)

### Generating Services

### Generating Module File
_generate_module_py(ros_learning
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ros_learning
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(ros_learning_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(ros_learning_generate_messages ros_learning_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingAction.msg" NAME_WE)
add_dependencies(ros_learning_generate_messages_py _ros_learning_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionGoal.msg" NAME_WE)
add_dependencies(ros_learning_generate_messages_py _ros_learning_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionResult.msg" NAME_WE)
add_dependencies(ros_learning_generate_messages_py _ros_learning_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingActionFeedback.msg" NAME_WE)
add_dependencies(ros_learning_generate_messages_py _ros_learning_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingGoal.msg" NAME_WE)
add_dependencies(ros_learning_generate_messages_py _ros_learning_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingResult.msg" NAME_WE)
add_dependencies(ros_learning_generate_messages_py _ros_learning_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/root/catkin_ws/devel/share/ros_learning/msg/LandingFeedback.msg" NAME_WE)
add_dependencies(ros_learning_generate_messages_py _ros_learning_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(ros_learning_genpy)
add_dependencies(ros_learning_genpy ros_learning_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS ros_learning_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ros_learning)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ros_learning
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_cpp)
  add_dependencies(ros_learning_generate_messages_cpp geometry_msgs_generate_messages_cpp)
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(ros_learning_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()
if(TARGET actionlib_msgs_generate_messages_cpp)
  add_dependencies(ros_learning_generate_messages_cpp actionlib_msgs_generate_messages_cpp)
endif()
if(TARGET mavros_msgs_generate_messages_cpp)
  add_dependencies(ros_learning_generate_messages_cpp mavros_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/ros_learning)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/ros_learning
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_eus)
  add_dependencies(ros_learning_generate_messages_eus geometry_msgs_generate_messages_eus)
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(ros_learning_generate_messages_eus std_msgs_generate_messages_eus)
endif()
if(TARGET actionlib_msgs_generate_messages_eus)
  add_dependencies(ros_learning_generate_messages_eus actionlib_msgs_generate_messages_eus)
endif()
if(TARGET mavros_msgs_generate_messages_eus)
  add_dependencies(ros_learning_generate_messages_eus mavros_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ros_learning)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ros_learning
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_lisp)
  add_dependencies(ros_learning_generate_messages_lisp geometry_msgs_generate_messages_lisp)
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(ros_learning_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()
if(TARGET actionlib_msgs_generate_messages_lisp)
  add_dependencies(ros_learning_generate_messages_lisp actionlib_msgs_generate_messages_lisp)
endif()
if(TARGET mavros_msgs_generate_messages_lisp)
  add_dependencies(ros_learning_generate_messages_lisp mavros_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/ros_learning)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/ros_learning
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_nodejs)
  add_dependencies(ros_learning_generate_messages_nodejs geometry_msgs_generate_messages_nodejs)
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(ros_learning_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()
if(TARGET actionlib_msgs_generate_messages_nodejs)
  add_dependencies(ros_learning_generate_messages_nodejs actionlib_msgs_generate_messages_nodejs)
endif()
if(TARGET mavros_msgs_generate_messages_nodejs)
  add_dependencies(ros_learning_generate_messages_nodejs mavros_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ros_learning)
  install(CODE "execute_process(COMMAND \"/usr/bin/python3\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ros_learning\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ros_learning
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_py)
  add_dependencies(ros_learning_generate_messages_py geometry_msgs_generate_messages_py)
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(ros_learning_generate_messages_py std_msgs_generate_messages_py)
endif()
if(TARGET actionlib_msgs_generate_messages_py)
  add_dependencies(ros_learning_generate_messages_py actionlib_msgs_generate_messages_py)
endif()
if(TARGET mavros_msgs_generate_messages_py)
  add_dependencies(ros_learning_generate_messages_py mavros_msgs_generate_messages_py)
endif()
