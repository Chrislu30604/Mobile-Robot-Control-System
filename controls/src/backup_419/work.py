import rospy
from util import *

def work_laser(conn, cmsg, handler=None):
    print(cmsg)
    message = handle_laser_data('0~180', 5)
    conn.send(message)
    message = handle_laser_data('540~720', 5)
    conn.send(message)

def work_enc(conn, cmsg, handler=None):
    global Rencoder, Lencoder
    message_enc = 'enc '
    message_enc += (str(Rencoder) + ' ' + str(Lencoder))
    print(message_enc)
    conn.send(message_enc)

def work_vel(conn, cmsg, handler=None):
    # TODO
    # Map C++ cmsg to python dictionary

    value = {
        'linear_x': 1,
        'linear_y': 0,
        'linear_z': 0,
        'ang_x': 0,
        'ang_y': 0,
        'ang_z': 0.3,
        'speed': 1,
        'turn': 1.
    }
    handler.update(**value)
