#!/bin/bash
# ================= 🚀 XTDrone 三机编队环境 (14580 标准版) =================
# 端口严格对齐:
#   MAVROS Bind (收): 14540+id  <-- PX4 发送 (mavlink_udp_port - 40)
#   MAVROS Remote (发): 14580+id --> PX4 监听 (mavlink_udp_port)
# =================================================================

export NO_AT_BRIDGE=1
export QT_X11_NO_MITSHM=1

RUN_DIR="$HOME/.xtdrone_multi_env"
mkdir -p "$RUN_DIR"

echo "📝 [0/5] 生成配置..."

gen_mavros() {
    id=$1
    port_bind=$((14540 + id))
    port_remote=$((14580 + id))  # 回归 14580
    tgt_sys_id=$((id + 1))
    
    cat << EOF > "$RUN_DIR/run_mavros_$id.sh"
#!/bin/bash
source /opt/ros/noetic/setup.bash
source ~/catkin_ws/devel/setup.bash
echo "🔗 连接 iris_$id (SysID:$tgt_sys_id Bind:$port_bind -> Remote:$port_remote)..."
rosrun mavros mavros_node \
    _fcu_url:="udp://:$port_bind@127.0.0.1:$port_remote" \
    _target_system_id:=$tgt_sys_id \
    __ns:=/iris_$id \
    __name:=mavros
EOF
}

# 依然保留通信脚本，但接下来的测试将尝试直连
gen_comm() {
    id=$1
    cat << EOF > "$RUN_DIR/run_comm_$id.sh"
#!/bin/bash
source /opt/ros/noetic/setup.bash
source ~/catkin_ws/devel/setup.bash
python3 ~/XTDrone/communication/multirotor_communication.py iris $id
EOF
}

for i in {0..2}; do
    gen_mavros $i
    gen_comm $i
done
chmod +x "$RUN_DIR/"*.sh

# 清理与启动
echo "🧹 [1/5] 清理..."
pkill -9 -f gazebo
pkill -9 -f rosmaster
pkill -9 -f px4
pkill -9 -f mavros
pkill -9 -f multirotor_communication
sleep 2

echo "🚀 [2/5] 启动 Gazebo..."
terminator -T "Sim_Display" -x bash -i -c "source ~/.bashrc; roslaunch px4 indoor3.launch; exec bash" &
sleep 40

echo "🔗 [3/5] 启动 MAVROS..."
for i in {0..2}; do
    "$RUN_DIR/run_mavros_$i.sh" > /dev/null 2>&1 &
    sleep 2
done
sleep 10

echo "🔧 [4/5] 注入参数..."
set_param() {
    id=$1
    param=$2
    val=$3
    for try in {1..3}; do
        rosrun mavros mavparam -n /iris_$id/mavros set $param $val > /dev/null 2>&1
        if [ $? -eq 0 ]; then return; fi
        sleep 1
    done
}

for i in {0..2}; do
    echo "Configuring iris_$i..."
    set_param $i COM_RCL_EXCEPT 4
    set_param $i COM_RC_IN_MODE 1
    set_param $i NAV_RCL_ACT 0
    set_param $i COM_ARM_WO_GPS 1
    set_param $i CBRK_IO_SAFETY 22027
done

echo "💻 [5/5] 启动通信..."
for i in {0..2}; do
    "$RUN_DIR/run_comm_$i.sh" > /dev/null 2>&1 &
done
sleep 2

terminator -T "Swarm_Control_Center" -x bash -i -c "
source /opt/ros/noetic/setup.bash; 
source ~/catkin_ws/devel/setup.bash; 
clear;
echo '✅ 端口重置为标准 14580';
echo '👉 请运行: python3 ~/catkin_ws/src/ros_learning/scripts/direct_swarm_control.py';
exec bash" &
EOF