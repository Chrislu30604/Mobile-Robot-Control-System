import rospy
import threading
from geometry_msgs.msg import Twist

sem = threading.Semaphore()
laser_data = []
Rencoder = 0
Lencoder = 0


class WalkWheel():
    def __init__(self, pub_vel):
        self.pub_vel = pub_vel
        self.twist = Twist()

    def run(self):
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            sem.acquire()
            # rospy.loginfo(self.twist)
            self.pub_vel.publish(self.twist)
            sem.release()
            rate.sleep()

    def update(self, **param):
        sem.acquire()
        try:
            speed = param.get('speed')
            turn = param.get('turn')
            self.twist.linear.x = param.get('linear_x') * speed
            self.twist.linear.y = param.get('linear_y') * speed
            self.twist.linear.z = param.get('linear_z') * speed
            self.twist.angular.x = param.get('ang_x') * turn
            self.twist.angular.y = param.get('ang_y') * turn
            self.twist.angular.z = param.get('ang_z') * turn
        except KeyError as error:
            rospy.logfatal('Require correct arugment', error)
        finally:
            sem.release()

    def stop(self):
        rospy.loginfo("Stop")
        self.pub_vel.publish(Twist())


""" Call Back Function
"""


def callback_laser(msg):
    global laser_data 
    laser_data = msg.ranges


def callback_Rencoder(msg):
    global Rencoder 
    Rencoder = msg.data


def callback_Lencoder(msg):
    global Lencoder 
    Lencoder = msg.data


def handle_laser_data(ranges, decimal):
    global laser_data
    try:
        assert(ranges == '0~180' or ranges == '540~720')
    except AssertionError as e:
        rospy.logfatal("Wrong Range 0-180, 540-720 ", e)
    print(laser_data)
    if ranges == '0~180':
	    message = '0~180 '
	    for i in range(180):
		print(i)
		message += (str(laser_data[i])[:decimal] + ' ')
	    rospy.loginfo('Send Laserdata 0~180')

    elif ranges == '540~720':
	    message = '540~720 '
	    for i in range(180):
		    message += (str(laser_data[540+i])[:decimal] + ' ')
	    rospy.loginfo('Send Laserdata 540~720')
    return message
