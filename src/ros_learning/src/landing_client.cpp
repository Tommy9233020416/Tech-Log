#include <ros/ros.h>
#include <actionlib/client/simple_action_client.h>
#include <ros_learning/LandingAction.h> // 替换为你的包名

typedef actionlib::SimpleActionClient<ros_learning::LandingAction> Client;

// 这是一个简单的“触发器”节点
int main(int argc, char** argv) {
    ros::init(argc, argv, "landing_trigger_node");
    
    // 连接到名为 "landing_action" 的服务器
    Client client("landing_action", true);

    ROS_INFO("Waiting for Drone Action Server...");
    client.waitForServer(); 
    ROS_INFO("Connected! Sending Landing Command...");

    // 设定降落目标：回到 (0,0) 点，高度降为 0
    ros_learning::LandingGoal goal;
    goal.target_x = 0;
    goal.target_y = 0;
    goal.target_z = 0.0; // 地面

    // 发送指令
    client.sendGoal(goal);
    
    ROS_INFO("Command Sent. Waiting for result...");
    
    // 等待结果（这里虽然会阻塞，但我们只是个触发器，无所谓）
    client.waitForResult();

    if (client.getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
        ROS_INFO("Drone reported: Landing Successful!");
    else
        ROS_INFO("Drone reported: Landing Failed or Preempted.");

    return 0;
}