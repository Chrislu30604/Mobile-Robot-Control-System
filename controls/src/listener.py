# -*- coding: utf-8 -*-
""" Listener for Remote Client send Request

The module define the object ClientThread hold the port and ip for multithreading.
Can Register specific JOB

TODO:
    Try catch
"""
import socket
import rospy
from threading import Thread


class Listener(Thread):
    """ Listener Class.
    The Class register by ip, port and run by start

    Note:
        max_client need to consider        
    Args:
        ip : default is localhost
        port : default is http/80/tcp
    """

    def __init__(self, job, ip='127.0.0.1', port=80, handler=None, max_client=1):
        Thread.__init__(self)
        self.job = job
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.ip, self.port))
        self.sock.listen(max_client)
        self.handler = handler
        rospy.loginfo("Start job {} on {}:{}".format(
            self.job, self.ip, self.port))

    def run(self):
        rospy.loginfo("Running {}:{}".format(self.ip, self.port))
        (conn, address) = self.sock.accept() # wait
        rospy.loginfo("{} accepted from {}".format(self.job, address))
        while True:
            try:
                cl_msg = conn.recv(1024)
                cl_msg = cl_msg.rstrip(' \t\r\n\0')
                cmsg = cl_msg.split()
                self.job(conn, cmsg, self.handler)
            except Exception:
                rospy.logfatal(Exception)
