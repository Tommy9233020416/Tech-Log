#include <ros/ros.h>
#include <geometry_msgs/PoseStamped.h>
#include <mavros_msgs/CommandBool.h>
#include <mavros_msgs/SetMode.h>
#include <mavros_msgs/State.h>
#include <cmath>
#include <actionlib/server/simple_action_server.h>
#include <ros_learning/LandingAction.h> // 确保包名正确
#include <tf2/LinearMath/Quaternion.h>
#include <tf2_geometry_msgs/tf2_geometry_msgs.h>


// --- 全局变量 ---
mavros_msgs::State current_state;
geometry_msgs::PoseStamped current_pose;
ros::Publisher local_pos_pub; // 全局发布者
bool is_landing_active = false; // [修改1] 新增：状态标志位，防止打架
bool is_mission_finished = false; // [修改1] 新增：结束标志位，防止重启

// --- 回调函数 ---
void state_cb(const mavros_msgs::State::ConstPtr& msg){
    current_state = *msg;
}

void pose_cb(const geometry_msgs::PoseStamped::ConstPtr& msg){
    current_pose = *msg;
}

typedef actionlib::SimpleActionServer<ros_learning::LandingAction> Server;

/**
 * Body 坐标系转 World 坐标系计算器
 * @param forward  向前飞多少米 (Body X)
 * @param left     向左飞多少米 (Body Y)
 * @param up       向上飞多少米 (Body Z)
 * @return         在 Map 坐标系下的目标点 Pose
 */
geometry_msgs::PoseStamped get_offset_pose(float forward, float left, float up) {
    geometry_msgs::PoseStamped target_pose;
    target_pose.header.frame_id = "map";
    target_pose.header.stamp = ros::Time::now();

    // 1. 获取当前姿态的四元数 (从全局变量 current_pose 中拿)
    tf2::Quaternion q;
    tf2::fromMsg(current_pose.pose.orientation, q);

    // 2. 定义相对位移向量 (Body Frame)
    // 比如：向前 2 米 -> (2.0, 0, 0)
    tf2::Vector3 offset_body(forward, left, up);

    // 3. 【核心魔法】 旋转向量！
    // 公式：NewVector = Quaternion * OldVector
    // 这行代码顶替了你刚才脑子里那个复杂的矩阵乘法
    tf2::Vector3 offset_map = tf2::quatRotate(q, offset_body);

    // 4. 加上当前的绝对位置
    target_pose.pose.position.x = current_pose.pose.position.x + offset_map.x();
    target_pose.pose.position.y = current_pose.pose.position.y + offset_map.y();
    target_pose.pose.position.z = current_pose.pose.position.z + offset_map.z();

    // 5. 保持姿态不变 (目标点的朝向 = 当前朝向)
    target_pose.pose.orientation = current_pose.pose.orientation;

    return target_pose;
}

// --- Action 执行回调 (降落逻辑) ---
void execute_landing(const ros_learning::LandingGoalConstPtr& goal, Server* as) {
    ROS_INFO("Action Received: Start Landing...");
    
    // [修改2] 上锁！告诉 main 循环：“我要接管控制权，你别说话”
    is_landing_active = true; 

    ros::Rate rate(20.0);
    ros_learning::LandingFeedback feedback;
    ros_learning::LandingResult result;
    bool success = true;

    geometry_msgs::PoseStamped land_pose;
    land_pose.header.frame_id = "map";

    // 降落循环
    while(ros::ok()) {
        if (as->isPreemptRequested() || !ros::ok()) {
            ROS_INFO("Preempted");
            as->setPreempted();
            success = false;
            break;
        }

        // 持续发布降落指令 (圆心, 高度0)
        land_pose.header.stamp = ros::Time::now();
        land_pose.pose.position.x = goal->target_x;
        land_pose.pose.position.y = goal->target_y;
        land_pose.pose.position.z = goal->target_z; 

        local_pos_pub.publish(land_pose);

        // 发布反馈
        feedback.current_z = current_pose.pose.position.z;
        as->publishFeedback(feedback);

        // 判断落地 (高度 < 0.2m)
        if(std::abs(current_pose.pose.position.z - goal->target_z) < 0.2) {
            ROS_INFO("Touchdown!");
            break;
        }

        ros::spinOnce();
        rate.sleep();
    }

    if(success) {
        result.success = true;
        as->setSucceeded(result);
        ROS_INFO("Landing Action Finished.");
        
        // [修改3] 任务永久结束，不要再起飞了
        is_mission_finished = true; 
    }
    
    // 释放锁 (虽然 finished 为 true 后 main 也就退出了，但养成好习惯)
    is_landing_active = false; 
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "drone_circle_node");
    ros::NodeHandle nh;
    ros::NodeHandle private_nh("~");

    ros::Subscriber state_sub = nh.subscribe<mavros_msgs::State>("mavros/state", 10, state_cb);
    ros::Subscriber local_pos_sub = nh.subscribe<geometry_msgs::PoseStamped>("mavros/local_position/pose", 10, pose_cb);
    local_pos_pub = nh.advertise<geometry_msgs::PoseStamped>("mavros/setpoint_position/local", 10);
    
    ros::ServiceClient arming_client = nh.serviceClient<mavros_msgs::CommandBool>("mavros/cmd/arming");
    ros::ServiceClient set_mode_client = nh.serviceClient<mavros_msgs::SetMode>("mavros/set_mode");

    Server server(nh, "landing_action", boost::bind(&execute_landing, _1, &server), false);
    server.start();

    ros::Rate rate(20.0);

    ROS_INFO("Waiting for connection...");
    while(ros::ok() && !current_state.connected){ ros::spinOnce(); rate.sleep(); }
    
    geometry_msgs::PoseStamped pose;
    pose.header.frame_id = "map";
    pose.pose.position.x = 0; pose.pose.position.y = 0; pose.pose.position.z = 2.0;

    // Warmup
    for(int i = 100; ros::ok() && i > 0; --i){
        pose.header.stamp = ros::Time::now();
        local_pos_pub.publish(pose);
        ros::spinOnce(); rate.sleep();
    }
    
    mavros_msgs::SetMode offb_set_mode;
    offb_set_mode.request.custom_mode = "OFFBOARD";
    mavros_msgs::CommandBool arm_cmd;
    arm_cmd.request.value = true;
    
    // 上锁指令 (任务结束后用)
    mavros_msgs::CommandBool disarm_cmd;
    disarm_cmd.request.value = false;

    ros::Time last_request = ros::Time::now();
    ros::Time last_jump_time = ros::Time::now();

    // 【修正】初始化为安全悬停点
    geometry_msgs::PoseStamped target_point = pose; 

    // --- 主循环 ---
    while(ros::ok()){
        // 1. 任务结束检查
        if (is_mission_finished) {
            if(current_state.armed && (ros::Time::now() - last_request > ros::Duration(5.0))) {
                arming_client.call(disarm_cmd);
                ROS_INFO("Mission Complete. Disarming...");
                last_request = ros::Time::now();
            }
            ros::spinOnce(); rate.sleep(); continue;
        }

        // 2. 降落中检查
        if (is_landing_active) {
            ros::spinOnce(); rate.sleep(); continue;
        }

        // 3. 解锁与切模式逻辑 (必须保留！)
        if( !current_state.armed && (ros::Time::now() - last_request > ros::Duration(5.0))){
            if( arming_client.call(arm_cmd) && arm_cmd.response.success){ ROS_INFO("Vehicle armed"); }
            last_request = ros::Time::now();
        } 
        else if( current_state.mode != "OFFBOARD" && (ros::Time::now() - last_request > ros::Duration(5.0))){
            if( set_mode_client.call(offb_set_mode) && offb_set_mode.response.mode_sent){ ROS_INFO("Offboard enabled"); }
            last_request = ros::Time::now();
        }

        // 4. 计算新的目标点 (Jump Logic)
        if (ros::Time::now() - last_jump_time > ros::Duration(5.0)) {
            // 每次基于【当前实际位置】向前跳
            target_point = get_offset_pose(2.0, 0.0, 1.5); 
            ROS_INFO("Jumping Forward! New Target: (%.2f, %.2f)", 
                     target_point.pose.position.x, target_point.pose.position.y);
            last_jump_time = ros::Time::now();
        }

        // 5. 发布指令
        target_point.header.stamp = ros::Time::now();
        local_pos_pub.publish(target_point);

        ros::spinOnce();
        rate.sleep();
    }
    return 0;
}