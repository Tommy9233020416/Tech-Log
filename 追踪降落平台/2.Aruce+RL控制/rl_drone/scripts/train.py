import rospy
from stable_baselines3 import PPO
from hover_env import HoverEnv

if __name__ == '__main__':
    # 1. 创建我们写好的环境
    env = HoverEnv()

    # 2. 实例化 PPO 算法
    # MlpPolicy: 多层感知机策略
    # device="cpu": 处理这几个坐标数字，CPU 比 GPU 更快
    model = PPO("MlpPolicy", env, verbose=1, device="cpu", tensorboard_log="./ppo_hover_tensorboard/")

    print("\n🚀 -----------------------------------")
    print("🚀 开始强化学习训练！请紧盯 Gazebo 画面！")
    print("🚀 -----------------------------------")
    
    # 3. 开始训练 (先试探性地训练 5000 步)
    # 按 Ctrl+C 可以随时中断
    try:
        model.learn(total_timesteps=50000)
    except KeyboardInterrupt:
        print("\n🛑 训练被手动终止。")

    # 4. 保存模型
    model.save("ppo_drone_hover")
    print("✅ 模型已保存为 ppo_drone_hover.zip")