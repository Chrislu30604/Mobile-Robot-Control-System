#! usr/bin/env python
import socket, sys, threading
import rospy
import string
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from std_msgs.msg import Int16
import myrostools

####### TCP IP setup ########
myhost = ''
myport = 1024
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if sock < 0:
        print 'Error: Cannot Create a Socket'
sock.bind((myhost, myport))
sock.listen(5);
print "Server_laser stands by";

myhost1 = ''
myport1 = 1025
sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if sock1 < 0:
        print 'Error: Cannot Create a Socket'
sock1.bind((myhost1, myport1))
sock1.listen(5);
print "Server_encoder stands by";
