import myrostools
import rospy

def worker_laser(conn, cmsg):
    message = myrostools.manage_laserdata('0~180', 5)
    conn.send(message)
    message = myrostools.manage_laserdata('540~720', 5)
    conn.send(message)

def worker_enc(conn, cmsg):
    message_enc = 'enc '
    message_enc += (str(myrostools.Rencoder) + ' ' + str(myrostools.Lencoder))
    conn.send(message_enc)

def worker_vel(conn, cmsg):
    try:	
        speed = float(cmsg[4])
        turn = float(cmsg[5])
        myrostools.twist.linear.x = float(cmsg[1]) * speed
        myrostools.twist.linear.y = float(cmsg[2]) * speed
        myrostools.twist.linear.z = 0
        myrostools.twist.angular.x = 0
        myrostools.twist.angular.y = 0
        myrostools.twist.angular.z = float(cmsg[3]) * turn
        rospy.debug('moving...')
    except Exception as e:
        rospy.logfatal(e)
