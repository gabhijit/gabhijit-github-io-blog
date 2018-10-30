# Implementing the same coroutine based echo server without busy waiting
# and using epoll to do non-blocking I/O

import collections
import socket
from types import GeneratorType
import sys

class ConnectionLost(Exception):
    pass

def listen_on(sock):
    while True:
        # get the next incoming connection
        # print "listen_on: before yield"
        connected_socket = nonblocking_accept(sock)
        val = yield connected_socket
        if val:
            print "connected_socket", val.fileno()

# Create a scheduler to manage all our coroutines
# Create a coroutine instance to run the echo_handler on
# incoming connections
#

def nonblocking_read(sock):
    """
    A coroutine that read's data in a non-blocking manner.
    """
    try:
        print "here", sock.fileno()
        data = sock.recv(1024)
        if data:
            print "*****Received Data*****:", "".join(data)
            yield Task(nonblocking_write(sock, data))

        if len(data) == 0:
            print "ConnectionLost"
            raise ConnectionLost("EOF")

        yield data

    except socket.error as e:
        yield Task(nonblocking_read(sock))
    except Exception as e:
        print e


def nonblocking_write(*args):

    try:
        sent = args[0].send(args[1])
        if sent == 0:
            raise ConnectionLost("EOF")
    except socket.error:
        sent = -1
    finally:
        yield sent

def nonblocking_accept(sock):

    #print "nonblocking_accept being called."
    try:
        value, _ = sock.accept()
        value.setblocking(False)
        print "sock", sock.fileno()
        print "value", value.fileno()
        return Task(echo_handler(value))
    except socket.error as e:
        return None

# coroutine function that echos data back on a connected
# socket
#
def echo_handler(sock):
    while True:
        try:
            yield Task(nonblocking_read(sock))
        except ConnectionLost:
            print "ConnectionLost"
            break
        except Exception as e:
            print e
            #pass  # exit normally if connection lost

def listening_socket(host, port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)
    sock.setblocking(False)

    return sock

listen_sock = listening_socket("localhost",7777)

server = listen_on(listen_sock)


class Task(object):
    task_id = 0
    def __init__(self, target, sendval=None):
        self.task_id = self.task_id + 1
        self.target = target
        self.sendval = sendval

    def run(self):
        print "target:", self.target.__name__, "isGenerator:", isinstance(self.target, GeneratorType)
        return self.target.send(self.sendval)


class Scheduler(object):

    def __init__(self):
        self.taskmap = {}
        self.runqueue = collections.deque()

    def schedule(self, task):
        self.runqueue.append(task)

    def loop(self):

        while len(self.runqueue) > 0:
            task = self.runqueue.popleft()
            result = task.run()
            #print "result:", result
            if isinstance(result, Task):
                self.schedule(result)
            if result is None:
                self.schedule(task)

s = Scheduler()

s.schedule(Task(server))

s.loop()

"""
Let's reason about this code

When 'listen_on' is added to the Trampoline at `t.add(server)`
`t.schedule(listen_on) get's called. This is going to first do a
listen_on.send(None) in the schedule and bring it to a point where it `yield`s
for the first time. ie. `yield nonblocking_accept(sock)` so the value
is now nonblocking_accept - coroutine object and that's added

and `t.run()` is run -
"""

