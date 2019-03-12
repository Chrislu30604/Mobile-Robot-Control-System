import myrostools
import rospy

def work_laser(conn, cmsg, handler=None):
    message = myrostools.manage_laserdata('0~180', 5)
    conn.send(message)
    message = myrostools.manage_laserdata('540~720', 5)
    conn.send(message)

def work_enc(conn, cmsg, handler=None):
    message_enc = 'enc '
    message_enc += (str(myrostools.Rencoder) + ' ' + str(myrostools.Lencoder))
    conn.send(message_enc)

def work_vel(conn, cmsg, handler=None):
    # TODO
    # Map C++ cmsg to python dictionary

    value = {
        'linear_x': 0,
        'linear_y': 0,
        'linear_z': 0,
        'ang_x': 0,
        'ang_y': 0,
        'ang_z': 0,
        'speed': 0,
        'turn': 0
    }
    handler.update(**value)
