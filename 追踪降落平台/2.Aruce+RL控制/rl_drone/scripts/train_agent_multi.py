#!/usr/bin/env python3
import os
import rospy
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.callbacks import CheckpointCallback
from drone_landing_env import DroneLandingEnv

def make_env(drone_id):
    """
    Utility function for multiprocess env.
    """
    def _init():
        # Each environment runs in its own spawned subprocess
        env = DroneLandingEnv(drone_id=drone_id, is_multiagent=True)
        return env
    return _init

if __name__ == '__main__':
    # Initialize main tracking node (optional, workers will init their own nodes)
    rospy.init_node('train_multi_agent', anonymous=True)
    os.makedirs('models', exist_ok=True)
    
    # We span 4 drones (iris_0 to iris_3) matching our launch file
    num_envs = 4
    env_fns = [make_env(i) for i in range(num_envs)]
    
    # Use SubprocVecEnv for true CPU isolation and parallel rollouts
    vec_env = SubprocVecEnv(env_fns)
    
    # Increase batch_size proportionally to the 4x environment capacity
    model = PPO("MlpPolicy", vec_env, verbose=1, learning_rate=3e-4, 
                n_steps=1024, batch_size=256, n_epochs=10, 
                tensorboard_log="./ppo_landing_tensorboard/", device="cuda")
                
    checkpoint_callback = CheckpointCallback(save_freq=5000, save_path='./models/',
                                             name_prefix='ppo_landing_multi')
                                             
    rospy.loginfo("Starting Multi-Agent Vectorized PPO Training...")
    try:
        model.learn(total_timesteps=500000, callback=checkpoint_callback)
    except KeyboardInterrupt:
        rospy.loginfo("Training interrupted by user, saving current model...")
        
    model.save("models/ppo_landing_multi_final")
    vec_env.close()
    rospy.loginfo("Training finished and model saved.")
