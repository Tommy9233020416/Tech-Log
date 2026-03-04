import rospy
import numpy as np  # <-- 核心修复：加上这一行
from stable_baselines3 import PPO
from hover_env import HoverEnv

if __name__ == '__main__':
    # 1. 实例化环境
    env = HoverEnv()

    # 2. 加载训练好的“大脑”
    print("🧠 正在加载模型：ppo_drone_hover.zip...")
    model = PPO.load("ppo_drone_hover")

    print("🚀 开始验收测试！观察 Gazebo 中的悬停表现...")
    
    obs, info = env.reset()
    
    try:
        while not rospy.is_shutdown():
            # deterministic=True 确保 AI 输出它认为最稳的动作
            action, _states = model.predict(obs, deterministic=True)
            
            # 执行动作
            obs, reward, terminated, truncated, info = env.step(action)
            
            # 实时打印当前高度和距离误差
            dist = np.linalg.norm(obs - env.target_pos)
            print(f"当前高度: {obs[2]:.2f}m | 距离误差: {dist:.2f}m | 奖励: {reward:.2f}")

            if terminated or truncated:
                print("🔄 触发重置，重新开始一轮测试...")
                obs, info = env.reset()
                
    except KeyboardInterrupt:
        print("\n🛑 测试已停止。")