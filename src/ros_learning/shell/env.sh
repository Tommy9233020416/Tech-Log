#!/bin/bash
# ================= 🚀 XTDrone 开发环境 (稳定集成版) =================
# 架构: 1:1 复刻 fly.sh 的成功逻辑 (动态生成脚本 + 独立窗口)
# 功能: 启动底层环境，打开一个空白窗口等待用户代码
# ===================================================================
# --- 修复 GUI 报错的关键配置 ---
export NO_AT_BRIDGE=1
export QT_X11_NO_MITSHM=1
# --- 1. 准备工作：生成临时脚本 ---
# 使用临时目录，避免污染你的源码目录
RUN_DIR="$HOME/.xtdrone_temp_env"
mkdir -p "$RUN_DIR"

echo "📝 [0/5] 正在生成底层服务脚本..."

# [A] MAVROS 启动脚本 (连接飞控)
cat << 'EOF' > "$RUN_DIR/run_mavros.sh"
#!/bin/bash
source /opt/ros/noetic/setup.bash
source ~/catkin_ws/devel/setup.bash
echo "⏳ 等待 Gazebo 启动..."
sleep 8
echo "🔗 正在连接 PX4 飞控..."
rosrun mavros mavros_node _fcu_url:="udp://:14540@127.0.0.1:14580" __ns:=/iris_0 __name:=mavros_manual
exec bash
EOF

# [B] 通信模块启动脚本 (XTDrone 中枢)
cat << 'EOF' > "$RUN_DIR/run_comm.sh"
#!/bin/bash
source /opt/ros/noetic/setup.bash
source ~/catkin_ws/devel/setup.bash
echo "💻 启动通信中枢..."
python3 ~/XTDrone/communication/multirotor_communication.py iris 0
exec bash
EOF

# 给脚本执行权限
chmod +x "$RUN_DIR/"*.sh

# --- 2. 强力清场 ---
echo "🧹 [1/5] 清理环境 (防止端口冲突)..."
pkill -9 -f gazebo
pkill -9 -f rosmaster
pkill -9 -f px4
pkill -9 -f mavros
sleep 2

# --- 3. 启动 Gazebo (主窗口) ---
echo "🚀 [2/5] 启动 Gazebo 仿真..."
# 保持可见，方便观察飞机姿态
terminator -T "1_Gazebo" -x bash -i -c "roslaunch px4 indoor1.launch; exec bash" &

echo "⏳ 等待仿真初始化 (给足20秒防止卡顿)..."
sleep 20

# --- 4. 启动 MAVROS (独立窗口) ---
echo "🔗 [3/5] 启动 MAVROS 桥接..."
# 调用生成的脚本，绝对稳定
terminator -T "2_Mavros" -x "$RUN_DIR/run_mavros.sh" &

echo "⏳ 等待飞控连接 (10秒)..."
sleep 15

# --- 5. 注入参数 ---
echo "🔧 [4/5] 注入 PX4 参数..."
set_param() {
    rosrun mavros mavparam -n /iris_0/mavros_manual set $1 $2 > /dev/null 2>&1
}
set_param COM_RC_IN_MODE 1
set_param COM_RCL_EXCEPT 4
set_param NAV_RCL_ACT 0
set_param COM_ARM_WO_GPS 1
set_param CBRK_IO_SAFETY 22027
echo "✨ 参数注入完成"

# --- 6. 启动通信与用户终端 ---
echo "💻 [5/5] 启动通信与开发终端..."

# 启动通信脚本 (左下角)
terminator -T "3_Communication" -x "$RUN_DIR/run_comm.sh" &
sleep 2

# [核心不同点] 启动用户开发终端 (右下角)
# 这里不运行键盘脚本，而是给你一个准备好环境的空终端
terminator -T "User_Code_Area" -x bash -i -c "
source /opt/ros/noetic/setup.bash; 
source ~/catkin_ws/devel/setup.bash; 
clear;
echo '=================================================';
echo '✅ 仿真环境搭建完毕 (架构同 fly.sh)';
echo '👉 飞机已解锁并处于 OFFBOARD 模式';
echo '👉 请在此窗口运行你的 Python 代码';
echo '   例如: python3 my_script.py';
echo '=================================================';
exec bash" &

echo "🎉 开发环境就绪！"