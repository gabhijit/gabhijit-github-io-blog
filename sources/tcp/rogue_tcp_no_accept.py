"""
A simple TCP server that listens on a socket and wait's in a while loop. We want to see how clients deal with it.
"""


import socket
import time

BIND_ADDRESS = "0.0.0.0"

if __name__ == '__main__':

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.bind(("0.0.0.0", 8080))

        x = sock.listen(100)

        while True:
            time.sleep(1000000)

    except Exception as e:
        print e

