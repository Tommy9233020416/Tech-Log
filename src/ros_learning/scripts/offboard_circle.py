#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import math
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State
from mavros_msgs.srv import CommandBool, CommandBoolRequest, SetMode, SetModeRequest

# 全局变量，用于存储当前飞控状态
current_state = State()

def state_cb(msg):
    global current_state
    current_state = msg

def offboard_circle():
    rospy.init_node('offboard_test_node', anonymous=True)

    # 1. 订阅状态话题，查看是否连接
    rospy.Subscriber("mavros/state", State, state_cb)

    # 2. 发布位置控制话题 (Local Position Setpoint)
    local_pos_pub = rospy.Publisher("mavros/setpoint_position/local", PoseStamped, queue_size=10)

    # 3. 定义服务客户端 (解锁和切模式)
    rospy.wait_for_service("/mavros/cmd/arming")
    arming_client = rospy.ServiceProxy("mavros/cmd/arming", CommandBool)

    rospy.wait_for_service("/mavros/set_mode")
    set_mode_client = rospy.ServiceProxy("mavros/set_mode", SetMode)

    # 设置发布频率 (必须 > 2Hz，建议 20Hz)
    rate = rospy.Rate(20.0)

    # 等待 MAVROS 连接到飞控
    while not rospy.is_shutdown() and not current_state.connected:
        rospy.loginfo("Waiting for FCU connection...")
        rate.sleep()

    # 初始化目标位置对象
    pose = PoseStamped()
    pose.pose.position.x = 0
    pose.pose.position.y = 0
    pose.pose.position.z = 10  # 目标高度 10米

    # --- 【新增】设置合法的姿态 (无旋转) ---
    pose.pose.orientation.x = 0
    pose.pose.orientation.y = 0
    pose.pose.orientation.z = 0
    pose.pose.orientation.w = 1.0  # 关键！w必须为1，代表"无旋转"

    # --- 关键步骤 ---
    # 在切换到 Offboard 模式之前，必须先发送一些设定点
    # 否则飞控会拒绝切换模式 (Failsafe)
    rospy.loginfo("Sending initial setpoints...")
    for i in range(100):
        if rospy.is_shutdown():
            break
        local_pos_pub.publish(pose)
        rate.sleep()

    # 创建请求对象
    offb_set_mode = SetModeRequest()
    offb_set_mode.custom_mode = 'OFFBOARD'

    arm_cmd = CommandBoolRequest()
    arm_cmd.value = True

    last_req = rospy.Time.now()
    
    # 记录起始时间用于计算圆周运动
    start_time = rospy.Time.now()

    # --- 主循环 ---
    while not rospy.is_shutdown():
        # 逻辑：每隔 5 秒尝试切一次模式/解锁，直到成功
        # 这样写是为了防止请求过于频繁阻塞通信
        if current_state.mode != "OFFBOARD" and (rospy.Time.now() - last_req) > rospy.Duration(5.0):
            if set_mode_client.call(offb_set_mode).mode_sent:
                rospy.loginfo("Offboard enabled")
            last_req = rospy.Time.now()
        else:
            if not current_state.armed and (rospy.Time.now() - last_req) > rospy.Duration(5.0):
                if arming_client.call(arm_cmd).success:
                    rospy.loginfo("Vehicle armed")
                last_req = rospy.Time.now()

        # --- 圆周运动算法 ---
        # 如果已经进入 Offboard 模式且解锁，开始计算圆的坐标
        if current_state.mode == "OFFBOARD" and current_state.armed:
            # 计算运行时间
            t = (rospy.Time.now() - start_time).to_sec()
            
            # 半径 10米
            radius = 10.0
            # 角速度 (rad/s)，0.2 大约是 2m/s 的线速度
            omega = 0.2 
            
            # 计算 x, y 坐标 (参数方程)
            pose.pose.position.x = radius * math.cos(omega * t)
            pose.pose.position.y = radius * math.sin(omega * t)
            pose.pose.position.z = 10.0  # 保持高度 10米

        # 发布目标位置
        local_pos_pub.publish(pose)

        rate.sleep()

if __name__ == '__main__':
    try:
        offboard_circle()
    except rospy.ROSInterruptException:
        pass