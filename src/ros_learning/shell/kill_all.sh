#!/bin/bash

echo "🚨 正在强制清理所有 ROS 和仿真进程..."
pkill -9 -f gazebo
pkill -9 -f rosmaster
pkill -9 -f px4
pkill -9 -f mavros
pkill -9 -f multirotor_communication
pkill -9 -f terminator
echo "✅ 清理完毕，系统应已恢复流畅。"
