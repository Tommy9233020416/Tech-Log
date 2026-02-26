# Project 1: 基于 PPO 算法的无人机自主悬停控制 (UAV RL Hover)

## 📖 项目背景
本项目作为具身智能（Embodied Intelligence）学习路径的首个阶段，旨在利用 **强化学习 (Deep Reinforcement Learning)** 替代传统的 PID 控制，实现无人机在三维仿真环境下的高精度定点悬停。

作为自动化专业大三学生的实践项目，本项目完整经历了从底层的 PX4 飞控环境搭建、MAVROS 通信链路调试，到上层 Gymnasium 强化学习环境构建的全过程。

---

## 🛠️ 技术栈
* **操作系统**: Ubuntu 20.04 (Docker 容器环境)
* **仿真引擎**: Gazebo 11 + PX4-Autopilot (SITL)
* **通信协议**: MAVROS (连接 ROS 与 PX4 的桥梁)
* **强化学习框架**: Stable-Baselines3 (PPO 算法)
* **观测/动作空间**: Gymnasium (自定义 `HoverEnv`)
* **可视化监控**: TensorBoard (实时监控收敛曲线)

---

## 🌟 核心工作与技术突破

### 1. 仿真环境自动化注入 (Security Bypass)
针对 PX4 飞控在无硬件遥控器时的安全锁定问题，开发了专用的 Launch 脚本。通过 `mavparam` 节点在系统启动后自动注入 `CBRK_SUPPLY_CHK` 和 `COM_RCL_EXCEPT` 等参数，成功绕过起飞预检，实现了全自动的 MAVROS 解锁流程。

### 2. 稳健的“上帝之手”物理重置机制
针对强化学习初期频繁出现的“翻机”导致飞控 EKF 崩溃的问题，实现了基于 Gazebo `SetModelState` 服务的物理纠偏逻辑。系统能够实时识别 `iris_0` 模型状态，并在重置时通过“瞬移”方式恢复姿态并清空物理惯性，极大提升了训练效率。

### 3. 混合动力起飞与状态交接
设计了一套“位置控制辅助起飞 + 速度控制 AI 接管”的平滑切换逻辑。通过监控无人机垂直高度，系统仅在高度稳定在 2m 目标点附近后才移交控制权给神经网络，解决了 RL Agent 在近地效应区难以起步的难题。

### 4. 奖励函数优化与对抗“自杀式刷分”
针对 Agent 早期通过快速自杀来减少累积扣分的“投机取巧”行为，对奖励函数进行了深度微调：
$$reward = 1.0 - (distance \times 0.5)$$
通过引入**生存奖励（Survival Bonus）**并结合较大的**死亡惩罚**，成功引导模型从“快速结束回合”转向“寻求长久悬停”。

---

## 📈 训练结果与可视化
经过约 20 万步的 PPO 训练，模型在 TensorBoard 中展现出明显的收敛趋势：
* **ep_rew_mean**: 经历了从发散到触底反弹的 V 字型曲线，最终奖励趋于稳定。
* **ep_len_mean**: 随着训练进行，无人机在空中的有效存活步数稳步提升，标志着模型掌握了基本的稳态控制能力。

---

## 📂 关键文件说明
* `launch/rl_hover.launch`: 整合了 Gazebo、PX4、MAVROS 及参数注入的一键启动脚本。
* `scripts/hover_env.py`: 封装了物理复位与交接逻辑的自定义 Gymnasium 环境类。
* `scripts/train.py`: PPO 算法训练脚本。
* `scripts/test_hover.py`: 加载 `.zip` 权重文件并在确定性模式下验证悬停精度的测试脚本。