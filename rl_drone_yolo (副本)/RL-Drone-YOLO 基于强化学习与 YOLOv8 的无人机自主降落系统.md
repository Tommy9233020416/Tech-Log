# RL-Drone-YOLO: 基于强化学习与 YOLOv8 的无人机自主降落系统

本项目实现了一个基于 **强化学习 (PPO)** 和 **YOLOv8** 目标检测的无人机自主降落系统。开发环境基于 **ROS Noetic**、**Gazebo** 和 **PX4 Autopilot** 仿真堆栈。

## 🚀 项目特性

- **YOLOv8 深度集成**：使用经过微调的 YOLOv8n 模型，实现对移动降落平台（Landing Pad）的实时高精度检测。
- **深度强化学习控制**：采用 PPO 算法（基于 Stable Baselines3）训练的控制策略，实现稳定精准的对准与降落。
- **采集训练全自动化**：内置全自动数据集采集、标注及 YOLO 模型微调脚本，无需手动干预。
- **鲁棒的搜索行为**：当目标超出视野（FOV）时，无人机会自动切换至“渐进式圆周搜索”模式，确保目标重捕获。
- **高度定制化仿真**：包含带下视摄像头的 iris 无人机模型及可移动的 Aruco 降落平台。

## 🛠️ 环境要求

- ROS Noetic (Ubuntu 20.04)
- PX4-Autopilot (SITL)
- MAVROS
- Python 3.8+
- PyTorch & Ultralytics (YOLOv8)
- Stable Baselines3 & Gymnasium

## 📦 安装指南

1. **克隆仓库**：
   ```bash
   cd ~/ros_ws/src
   git clone <您的仓库链接> rl_drone_yolo
   ```

2. **安装 Python 依赖项**：
   ```bash
   pip3 install ultralytics stable-baselines3 gymnasium opencv-python
   ```

3. **编译工作空间**：
   ```bash
   cd ~/ros_ws
   catkin_make
   source devel/setup.bash
   ```

## 🎮 使用方法

### 1. 启动仿真环境
启动 Gazebo、PX4 SITL 以及 MAVROS 节点（已配置 5 倍速加速）：
```bash
cd ~/ros_ws/src/rl_drone_yolo
./run_rl_sim.sh
```

### 2. 运行已训练的智能体
运行 RL 策略进行自主降落演示：
```bash
cd ~/ros_ws/src/rl_drone_yolo/scripts
python3 enjoy.py
```

### 3. 数据采集与模型训练
如果您需要重新训练系统：
- **采集数据**：`python3 collect_data.py`（自动获取带真值标注的样张）。
- **微调 YOLO**：`python3 train_yolo.py`（在采集的数据集上进行微调）。
- **训练 RL 策略**：`python3 train_agent.py`（训练 PPO 降落控制模型）。

## 📂 项目结构

- `launch/`：仿真环境及各功能节点的 ROS 启动文件。
- `models/`：自定义模型文件（包含 `iris_yolo` 无人机及 `aruco_pad` 平台）。
- `scripts/`：
  - `drone_landing_env.py`：封装了 ROS/MAVROS 通信的极简 Gymnasium 环境。
  - `yolo_detector.py`：YOLOv8 推理节点，发布目标归一化位置。
  - `collect_data.py`：**核心工具**，自动根据坐标投影生成精准标注的数据集。
  - `enjoy.py`：RL 策略测试脚本。
- `worlds/`：Gazebo 仿真世界描述文件。

## 📝 关键参数说明

- **检测阈值**：在 `yolo_detector.py` 中默认为 0.2，以适应专用微调模型。
- **控制频率**：RL 动作指令以 10Hz 频率发布。
- **稳定性增强**：针对加速仿真优化了 EKF 的稳定等待逻辑。
