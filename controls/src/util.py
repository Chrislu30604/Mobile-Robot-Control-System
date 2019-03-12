import rospy
import threading
from geometry_msgs.msg import Twist

sem = threading.Semaphore()

class WalkWheel():
    def __init__(self, pub_vel):
        self.pub_vel = pub_vel
        self.twist = Twist()

    def run(self):
        rate = rospy.Rate(10)
        while True:
            sem.acquire()
            self.pub_vel.publish(self.twist)
            rate.sleep()
            sem.release()

    def update(self, **param):
        sem.acquire()
        try:
            speed = param('speed')
            turn = param('turn')
            self.twist.linear.x = param('linear_x') * speed
            self.twist.linear.y = param('linear_y') * speed   
            self.twist.linear.z = param('linear_z') * speed
            self.twist.angular.x = param('ang_x') * turn
            self.twist.angular.y = param('ang_y') * turn
            self.twist.angular.z = param('ang_z') * turn
        except KeyError:
            rasie KeyError('Require correct arugment')
        finally:
            sem.release()

    def stop(self):
        rospy.info("Stop")
        self.pub_vel.publish(Twist())