import sys
import time
import socket

def sendLaser():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ('localhost', 8001)
    print(f"connection on {address}")
    sock.connect(address)

    message = b"send laser"
    while(True):
        print('send')
        time.sleep(1)
        sock.sendall(message)

def main():
    sendLaser()


if __name__ == "__main__":
    main()