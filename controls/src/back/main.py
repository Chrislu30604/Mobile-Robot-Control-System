#!/usr/bin/env python
import rospy
import sys
import socket

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from std_msgs.msg import Int16

import myrostools
from work import *
from listener import Listener

HOST = '192.168.31.200'
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
    sub_laser = rospy.Subscriber('/scan', LaserScan, myrostools.callback_laser); 
    sub_Renc = rospy.Subscriber('/Rencoder', Int16, myrostools.callback_Rencoder);
    sub_Lenc = rospy.Subscriber('/Lencoder', Int16, myrostools.callback_Lencoder);
    # Publishes
    pub_vel = myrostools.pub_vel

    # Thread Pooooooool
    laser_t = Listener(work_laser, HOST, PORT['LASER'])
    enc_t = Listener(work_enc, HOST, PORT['ENC'])
    vel_t = Listener(work_vel, HOST, PORT['VEL'])
    threadManger = [laser_t, enc_t, vel_t] # Wrapper

    while not rospy.is_shutdown():
        map(lambda obj:(obj.setDaemon(True), obj.start()), threadManger)
        rospy.spin()


if __name__ == '__main__':
    main()
