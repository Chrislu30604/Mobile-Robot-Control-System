import rospy
import util


dataHolder = util.DataHolder()

def work_laser(conn, cmsg, handler=None):
    print(cmsg)
    message = handle_laser_data('0~180', 5)
    conn.send(message)
    message = handle_laser_data('540~720', 5)
    conn.send(message)

def work_enc(conn, cmsg, handler=None):
    message_enc = 'enc '
    message_enc += (str(dataHolder.rencoder) + ' ' + str(dataHolder.lencoder))
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


"""
    Callback function
"""
def callback_laser(msg):
    dataHolder.laser_data = msg.ranges


def callback_Rencoder(msg):
    dataHolder.rencoder = msg.data


def callback_Lencoder(msg):
    dataHolder.lencoder = msg.data


def handle_laser_data(ranges, decimal):
    try:
        assert(ranges == '0~180' or ranges == '540~720')
    except AssertionError as e:
        rospy.logfatal("Wrong Range 0-180, 540-720 ", e)
    
    data = dataHolder.laser_data

    if ranges == '0~180':
        message = '0~180 ' + "".join(format(x, ".5f") for x in data[:180])
        """
        for i in range(180):
            message += (str(data[i])[:decimal] + ' ')
        """
        rospy.loginfo('Send Laserdata 0~180')

    elif ranges == '540~720':
        message = '540~720 ' + "".join(format(x, ".5f") for x in data[540:])
        """
        for i in range(180):
            message += (str(data[540+i])[:decimal] + ' ')
        """
        rospy.loginfo('Send Laserdata 540~720')
    return message
