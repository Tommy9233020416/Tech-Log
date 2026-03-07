#!/usr/bin/env python3
from ultralytics import YOLO
import argparse
import os

def train():
    # Load a model
    model = YOLO("yolov8n.pt")  # load a pretrained model
    
    # Train the model
    results = model.train(
        data="/root/ros_ws/src/rl_drone_yolo/scripts/pad_data.yaml",
        epochs=100,
        imgsz=320,
        batch=16,
        workers=0,  # Avoid SHM bus errors by using 0 workers
        name="pad_yolo_finetune",
        project="/root/ros_ws/src/rl_drone_yolo/scripts/runs"
    )
    
    print(f"Training complete. Results saved to {results.save_dir}")

if __name__ == "__main__":
    train()
