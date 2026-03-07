#!/usr/bin/env python3
import os
import rospy
import glob
import subprocess
import time
import zipfile
import sys
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from typing import Callable
from drone_landing_env import DroneLandingEnv

LATEST_MODEL_DIR = "models/"
LATEST_MODEL_PREFIX = "ppo_landing_"

def linear_schedule(initial_value: float) -> Callable[[float], float]:
    """
    Linear learning rate schedule.
    :param initial_value: Initial learning rate.
    :return: schedule that computes current learning rate depending on remaining progress
    """
    def func(progress_remaining: float) -> float:
        """
        Progress will decrease from 1 (beginning) to 0.
        Decay from 3e-4 down to 1e-5 (so it never hits exactly 0).
        """
        min_lr = 1e-5
        return progress_remaining * (initial_value - min_lr) + min_lr
    return func

def get_latest_model():
    """Finds the most recently saved model in the models/ directory."""
    list_of_files = glob.glob(f"{LATEST_MODEL_DIR}{LATEST_MODEL_PREFIX}*.zip")
    if not list_of_files:
        return None
        
    # Sort files by creation time, newest first
    list_of_files.sort(key=os.path.getctime, reverse=True)
    
    for file_path in list_of_files:
        try:
            with zipfile.ZipFile(file_path) as zf:
                if zf.testzip() is None:
                    return file_path
        except zipfile.BadZipFile:
            print(f"Skipping corrupted archive: {file_path}")
            continue
            
    return None

def wait_for_env():
    """Checks if ROS Master and environment are up."""
    print("⏳ Waiting for Gazebo environment to be started by the user...")
    while True:
        gazebo_alive = False
        try:
            # Check if rosmaster and gazebo are running
            # subprocess.run is safer than check_output to avoid unhandled exit code traces
            result = subprocess.run(["rosnode", "list"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0 and "/gazebo" in result.stdout:
                gazebo_alive = True
        except Exception:
            pass
            
        if gazebo_alive:
            print("✅ Gazebo environment is running and ready!")
            return
            
        time.sleep(5)

def start_training():
    # Ensure models dir exists
    os.makedirs(LATEST_MODEL_DIR, exist_ok=True)
    
    # 0. Make sure the world is alive before ANYTHING else
    wait_for_env()
    
    # Needs to be called once before any rospy interaction!
    try:
        rospy.init_node("rl_drone_trainer", anonymous=True)
    except Exception:
        print("rospy.init_node already called.")
        
    print("Starting PPO Training/Execution Loop with Auto-Restart Mechanism...")
    
    while True:
        # Check if environment died and needs reboot
        wait_for_env()
        
        # Check if a previous model exists to resume training
        latest_model_path = get_latest_model()
        
        # We instantiate a fresh environment every loop because the old one might be dead
        env = DroneLandingEnv()
        
        if latest_model_path:
            rospy.loginfo(f"🚀 Found existing model: {latest_model_path}. Loading weights to RESUME training...")
            try:
                model = PPO.load(latest_model_path, env=env, device="cuda")
            except Exception as e:
                rospy.logerr(f"CRITICAL ERROR: Failed to load model {latest_model_path}. The file might be corrupted by a power loss. Error: {e}")
                rospy.logwarn("Deleting the corrupted archive and restarting search for the next latest model...")
                os.remove(latest_model_path)
                env.close()
                continue
        else:
            rospy.loginfo("🌱 No previous model found. Starting FRESH training...")
            model = PPO("MlpPolicy", env, verbose=1, 
                        learning_rate=linear_schedule(3e-4),
                        n_steps=1024, batch_size=64, n_epochs=10, 
                        tensorboard_log="./ppo_landing_tensorboard/", device="cuda")
                        
        checkpoint_callback = CheckpointCallback(save_freq=5000, save_path=LATEST_MODEL_DIR,
                                                 name_prefix='ppo_landing')
        
        try:
            # Train indefinitely until a crash happens
            model.learn(total_timesteps=10000000, callback=checkpoint_callback, reset_num_timesteps=False)
            
        except Exception as e:
            rospy.logerr(f"CRITICAL ENV ERROR CAUGHT: {e}")
            rospy.loginfo("Saving brain state before environment crash...")
            
            # Save the latest state before it crashed
            model.save(f"{LATEST_MODEL_DIR}{LATEST_MODEL_PREFIX}emergency_save")
            
            # Close the dangling ROS environment handles
            env.close()
            
            rospy.logerr("⚠️ ENVIRONMENT CRASHED OR TIMED OUT! ⚠️")
            rospy.logerr("Auto-recovering: Killing simulation and relaunching python process...")
            
            subprocess.run("killall -9 gzserver gzclient roslaunch rosmaster px4 rosout >/dev/null 2>&1 || true", shell=True)
            time.sleep(5)
            
            subprocess.Popen(["/bin/bash", "run_rl_sim.sh"], cwd="/root/ros_ws/src/rl_drone_yolo", start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(15)
            
            os.execv(sys.executable, ['python3'] + sys.argv)

        except KeyboardInterrupt:
            rospy.loginfo("Training interrupted by user, saving current model...")
            model.save(f"{LATEST_MODEL_DIR}{LATEST_MODEL_PREFIX}final")
            rospy.loginfo("Training finished and model saved.")
            break

if __name__ == '__main__':
    start_training()
