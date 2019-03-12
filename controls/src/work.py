import myrostools
import rospy

from util import *

def work_laser(conn, cmsg, handler=None):
    message = handle_laser_data('0~180', 5)
    conn.send(message)
    message = handle_laser_data('540~720', 5)
    conn.send(message)

def work_enc(conn, cmsg, handler=None):
    message_enc = 'enc '
    message_enc += (str(Rencoder) + ' ' + str(Lencoder))
    conn.send(message_enc)

def work_vel(conn, cmsg, handler=None):
    # TODO
    # Map C++ cmsg to python dictionary

    value = {
        'linear_x': 10,
        'linear_y': 10,
        'linear_z': 0,
        'ang_x': 0,
        'ang_y': 0,
        'ang_z': 10,
        'speed': 10,
        'turn': 10
    }
    handler.update(**value)
