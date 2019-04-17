import rospy
import threading
from geometry_msgs.msg import Twist

sem = threading.Semaphore()

class DataHolder(object):

    def __init__(self, laser_data=[1, 2, 3], rencoder=0, lencoder=0):
        self._laser_data = laser_data
        self._rencoder = rencoder
        self._lencoder = lencoder
    
    @property
    def laser_data(self):
        return self._laser_data
    
    @property
    def rencoder(self):
        return self._rencoder

    @property
    def lencoder(self):
        return self._lencoder

    @laser_data.setter
    def laser_data(self, new_laser_data):
        self._laser_data = new_laser_data

    @rencoder.setter
    def rencoder(self, new_rencoder):
        self._rencoder = new_rencoder

    @lencoder.setter
    def lencoder(self, new_lencoder):
        self._lencoder = new_lencoder


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
