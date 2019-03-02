# -*- coding: utf-8 -*-
""" ClientThread for specific object

The module define the object ClientThread hold the port and ip for multithreading.

Todo:
    Try catch
"""
import socket
import rospy
from threading import Thread

class Listener(Thread):
    
    def __init__(self, job, ip='127.0.0.1', port=80, max_client=1):
        Thread.__init__(self)
        self.job = job
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.ip, self.port))
        self.sock.listen(max_client)
        rospy.loginfo("Start job {} on {}:{}".format(self.job, self.ip, self.port))

    def run(self):
        rospy.loginfo("Running {}:{}".format(self.ip, self.port))
        while True:
            (conn, address) = self.sock.accept()
            rospy.loginfo("{} accepted from {}".format(self.job, address))
            cl_msg = conn.recv(1024)
            cl_msg = cl_msg.rstrip(' \t\r\n\0')
            cmsg = cl_msg.split()
            self.job(conn, cmsg)
