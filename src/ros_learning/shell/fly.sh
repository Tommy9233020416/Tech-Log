#!/bin/bash
# ================= 🚀 XTDrone 全能启动脚本 (All-in-One) =================
# 原理: 脚本运行时自动生成临时启动文件，规避 Terminator 的引号转义 Bug
# 功能: 清场 -> 生成辅助脚本 -> 启动四个独立窗口 -> 自动配置参数
# ======================================================================

# --- 1. 准备工作：创建临时运行目录 ---
# 我们把辅助脚本生成在隐藏目录里，你看不到，也就不会觉得烦
RUN_DIR="$HOME/.xtdrone_temp_run"
mkdir -p "$RUN_DIR"

echo "📝 [0/5] 正在生成运行时脚本..."

# --- 2. 动态生成 MAVROS 启动脚本 ---
cat << 'EOF' > "$RUN_DIR/run_mavros.sh"
#!/bin/bash
# 显式加载环境，不依赖 .bashrc
source /opt/ros/noetic/setup.bash
source ~/catkin_ws/devel/setup.bash
echo "⏳ 等待 Gazebo 就绪..."
sleep 8
echo "🔗 正在连接 PX4 飞控..."
# 启动 MAVROS 节点 (连接 14540 <-> 14580)
rosrun mavros mavros_node _fcu_url:="udp://:14540@127.0.0.1:14580" __ns:=/iris_0 __name:=mavros_manual
exec bash
EOF

# --- 3. 动态生成 通信 启动脚本 ---
cat << 'EOF' > "$RUN_DIR/run_comm.sh"
#!/bin/bash
source /opt/ros/noetic/setup.bash
source ~/catkin_ws/devel/setup.bash
echo "💻 启动通信脚本..."
# 直接运行，不再会有引号问题
python3 ~/XTDrone/communication/multirotor_communication.py iris 0
exec bash
EOF

# --- 4. 动态生成 键盘 启动脚本 ---
cat << 'EOF' > "$RUN_DIR/run_key.sh"
#!/bin/bash
source /opt/ros/noetic/setup.bash
source ~/catkin_ws/devel/setup.bash
echo "🎮 启动键盘控制..."
# 同样直接运行
python3 ~/XTDrone/control/keyboard/multirotor_keyboard_control.py iris 1 vel
exec bash
EOF

# 给所有生成的脚本赋予执行权限
chmod +x "$RUN_DIR/"*.sh

# =================== 执行阶段 ===================

# --- 5. 环境清场 ---
echo "🧹 [1/5] 清理残留进程..."
pkill -9 -f gazebo
pkill -9 -f rosmaster
pkill -9 -f px4
pkill -9 -f mavros
sleep 2

# --- 6. 启动 Gazebo (主窗口) ---
echo "🚀 [2/5] 启动 Gazebo 仿真..."
# 主窗口依然用 bash -i 加载你的配置，因为它需要运行 roslaunch
terminator -T "1_Gazebo" -x bash -i -c "roslaunch px4 indoor1.launch; exec bash" &

echo "⏳ 等待仿真初始化 (20秒)..."
sleep 20

# --- 7. 启动 MAVROS (独立窗口) ---
echo "🔗 [3/5] 启动 MAVROS 桥接..."
# 直接调用生成的脚本文件，绝对稳定
terminator -T "2_Mavros" -x "$RUN_DIR/run_mavros.sh" &

echo "⏳ 等待飞控连接 (20秒)..."
sleep 20

# --- 8. 注入参数 (直接在当前脚本运行) ---
echo "🔧 [4/5] 注入 PX4 安全参数..."
# 定义一个函数来静默设置参数
set_param() {
    rosrun mavros mavparam -n /iris_0/mavros_manual set $1 $2 > /dev/null 2>&1
}

set_param COM_RC_IN_MODE 1
set_param COM_RCL_EXCEPT 4
set_param NAV_RCL_ACT 0
set_param NAV_DLL_ACT 0
set_param COM_ARM_WO_GPS 1
set_param CBRK_IO_SAFETY 22027

echo "✨ 参数注入完成"

# --- 9. 启动通信与控制 (独立窗口) ---
echo "💻 [5/5] 启动控制终端..."
terminator -T "3_Communication" -x "$RUN_DIR/run_comm.sh" &
sleep 2

terminator -T "4_Keyboard" -x "$RUN_DIR/run_key.sh" &

echo "🎉 系统全部就绪！请点击 [4_Keyboard] 窗口操作：按 'b' 切模式 -> 按 'i' 起飞"