import rospy
from hover_env import HoverEnv
from stable_baselines3.common.env_checker import check_env

if __name__ == '__main__':
    print("⏳ 正在初始化测试环境...")
    env = HoverEnv()
    
    print("🔍 开始验证 Gym 接口规范...")
    check_env(env)
    print("✅ 环境验证通过！完全符合 Stable-Baselines3 标准。")
    
    print("\n🚀 开始模拟一步交互测试...")
    obs, info = env.reset()
    print(f"📍 初始观测状态 (XYZ): {obs}")
    
    action = env.action_space.sample() # 随机生成一个动作
    print(f"🕹️ 随机生成的动作指令 (XYZ速度): {action}")
    
    obs, reward, terminated, truncated, info = env.step(action)
    print(f"📍 执行后新状态: {obs}")
    print(f"💰 获得奖励: {reward:.2f}")