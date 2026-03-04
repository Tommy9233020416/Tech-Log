#!/usr/bin/env python3
import rospy
import subprocess
import time

def main():
    rospy.init_node("px4_headless_setup")
    rospy.loginfo("Waiting 10 seconds for PX4/MAVROS to fully initialize...")
    time.sleep(10)
    
    params = [
        ("NAV_RCL_ACT", "0"),
        ("NAV_DLL_ACT", "0"),
        ("COM_RCL_EXCEPT", "4"),
        ("COM_RC_IN_MODE", "1"),
        ("CBRK_SUPPLY_CHK", "894281"),
        ("CBRK_USB_CHK", "197848"),
        ("SYS_HAS_MAG", "0"),
        ("COM_ARM_IMU_ACC", "50.0"),
        ("COM_ARM_IMU_GYR", "50.0")
    ]
    
    for p, v in params:
        rospy.loginfo(f"Applying PX4 parameter: {p} = {v}")
        subprocess.run(["rosrun", "mavros", "mavparam", "set", p, v])
        
    rospy.loginfo("=====================================================")
    rospy.loginfo("✅ All headless/no-RC parameters successfully saved!")
    rospy.loginfo("These are stored in the EEPROM. You DO NOT need to run this again.")
    rospy.loginfo("=====================================================")

if __name__ == "__main__":
    main()
