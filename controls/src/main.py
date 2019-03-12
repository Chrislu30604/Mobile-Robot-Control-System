#!/usr/bin/env python
import rospy
import sys
import socket

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from std_msgs.msg import Int16

import myrostools
from util import WalkWheel
from work import *
from listener import Listener

HOST = ''
PORT = {
    'LASER':8001,
    'ENC'  :8002,
    'VEL'  :8003  
}

def main():
    rospy.init_node("Scanner_Laser")
    rospy.loginfo("Start Running Node")
    rate = rospy.Rate(10)
    
    # Subscribe 
    sub_laser = rospy.Subscriber('/scan', LaserScan, myrostools.callback_laser)
    sub_Renc = rospy.Subscriber('/Rencoder', Int16, myrostools.callback_Rencoder)
    sub_Lenc = rospy.Subscriber('/Lencoder', Int16, myrostools.callback_Lencoder)
    # Publishes
    pub_vel = rospy.Publishes('cmd_vel', Twist, queue_size=1)
    walk_wheel = WalkWheel(pub_vel)

    # Thread Pooooooool
    laser_t = Listener(work_laser, HOST, PORT['LASER'])
    enc_t = Listener(work_enc, HOST, PORT['ENC'])
    vel_t = Listener(work_vel, HOST, PORT['VEL'], walk_wheel)
    threadManger = [laser_t, enc_t, vel_t] # Wrapper

    while not rospy.is_shutdown():
        map(lambda obj:(obj.setDaemon(True), obj.start()), threadManger)
        walk_wheel.run()

if __name__ == '__main__':
    main()
