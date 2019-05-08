#! /usr/bin/env python
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
print "Server stands by";

######## Set up ROS subcribers and publushers ####### 
rospy.init_node('scan_values')	# This node name.
rate = rospy.Rate(10);	# For publishers.
sub_laser = rospy.Subscriber('/scan', LaserScan, myrostools.callback_laser); 
sub_Renc = rospy.Subscriber('/Rencoder', Int16, myrostools.callback_Rencoder);
sub_Lenc = rospy.Subscriber('/Lencoder', Int16, myrostools.callback_Lencoder);
#pub_vel = rospy.Publisher('cmd_vel', Twist, queue_size=1);
pub_vel = myrostools.pub_vel;

move_vel_thread = myrostools.thread_vel();
move_vel_thread.start();

####### Main Function ########
while True:
	# connect to a client
	csock, address = sock.accept()
	print ('Client info: ', csock, address)

	# while -> keep receiving the message
	while True:
		cl_msg = csock.recv(1024);
		cl_msg = cl_msg.rstrip(' \t\r\n\0');
		cmsg = cl_msg.split();

		if cmsg[0] == 'laser':
			message = myrostools.manage_laserdata('0~180', 8);
			csock.send(message);
			message = myrostools.manage_laserdata('540~720', 8);
			csock.send(message);

		elif cmsg[0] == 'enc':
			message_enc = 'enc ';
			message_enc += (str(myrostools.Rencoder) + ' ' + str(myrostools.Lencoder));
			print 'Encoder: ', message_enc
			csock.send(message_enc);
		elif cmsg[0] == 'vel':
			# data type: [vel x y th speed angular_speed]
			try:	
				global move_vel_thread;
				move_vel_thread.pause();
				speed = float(cmsg[4]);
				turn = float(cmsg[5])
				myrostools.twist.linear.x = float(cmsg[1]) * speed;
				myrostools.twist.linear.y = float(cmsg[2]) * speed;
				myrostools.twist.linear.z = 0;
				myrostools.twist.angular.x = 0;
				myrostools.twist.angular.y = 0;
				myrostools.twist.angular.z = float(cmsg[3]) * turn;
				print 'moving...'
				move_vel_thread.resume();
			except Exception as e:
				print e;

		elif cmsg[0] == 'stop':
			twist1 = Twist();
			print 'stop!!'
			move_vel_thread.pause();
			pub_vel.publish(twist1);
			break;
#rospy.spin();
