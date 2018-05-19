"""
A Client sending data to a server that doesn't accept, we want to see what happens.
"""

import socket
import time

#SERVER_IP = "10.1.2.2"
SERVER_IP = "localhost"

if __name__ == '__main__':

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((SERVER_IP, 8080))

        data = "0" * 1200
        count = 1
        while True:
            written = sock.send(data)
            print written, count
            time.sleep(0.05)
            count += 1


    except Exception as e:
        print e
