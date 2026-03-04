import gymnasium as gym
from stable_baselines3 import PPO
import torch

# 1. 检查装备
print(f"🔥 正在使用设备: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")

# 2. 创建环境 (CartPole-v1: 倒立摆)
# render_mode="human" 会弹窗显示动画，让你看到训练过程
env = gym.make("CartPole-v1", render_mode="human")

# 3. 创建 PPO 模型
# MlpPolicy: 使用普通神经网络
# verbose=1: 打印训练日志
model = PPO("MlpPolicy", env, verbose=1, device="cuda")

# 4. 开始训练
print("🚀 开始训练... (按 Ctrl+C 可以提前停止)")
try:
    # 训练 10,000 步 (大概几十秒)
    model.learn(total_timesteps=10000)
except KeyboardInterrupt:
    print("\n训练被手动停止")

# 5. 保存模型
model.save("ppo_cartpole_model")
print("✅ 模型已保存为 ppo_cartpole_model.zip")

env.close()