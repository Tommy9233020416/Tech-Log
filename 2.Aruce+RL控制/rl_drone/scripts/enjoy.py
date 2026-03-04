#!/usr/bin/env python3
import gymnasium as gym
import rospy
from stable_baselines3 import PPO
from drone_landing_env import DroneLandingEnv

if __name__ == '__main__':
    rospy.init_node("enjoy_node", anonymous=True)
    env = DroneLandingEnv()
    
    # Load model
    try:
        model = PPO.load("models/ppo_landing_final")
        rospy.loginfo("Successfully loaded PPO model from models/ppo_landing_final")
    except Exception as e:
        rospy.logerr(f"No trained model found! Please run train_agent.py first. Error: {e}")
        exit(1)
        
    obs, info = env.reset()
    rospy.loginfo("Enjoying the trained policy...")
    
    while not rospy.is_shutdown():
        # Predict action
        action, _states = model.predict(obs, deterministic=True)
        # Execute action in environment
        obs, reward, terminated, truncated, info = env.step(action)
        
        if terminated or truncated:
            success_str = "SUCCESS" if info.get('is_success', False) else "FAILED"
            rospy.loginfo(f"Episode Done. Result: {success_str}")
            # Reset environment for next episode
            obs, info = env.reset()
            
