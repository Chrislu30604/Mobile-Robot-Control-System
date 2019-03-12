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
        while not rospy.is_shutdown():
            sem.acquire()
            print("__")
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
            rospy.Fatal('Require correct arugment', error)
        finally:
            sem.release()

    def stop(self):
        rospy.info("Stop")
        self.pub_vel.publish(Twist())
