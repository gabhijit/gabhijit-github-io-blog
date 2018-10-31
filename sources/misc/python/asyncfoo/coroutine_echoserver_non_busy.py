# Implementing the same coroutine based echo server without busy waiting
# and using epoll to do non-blocking I/O
# TODO: This is still busy waiting and more clean up is needed
#
# In fact I am just going to use things from Dave Beazley's talk.
# https://www.youtube.com/watch?v=MCs5OvhV9S4

import collections
import socket
from types import GeneratorType
import sys
import select

# Fugly - get rid of this when we do a proper select
import time

class ConnectionLost(Exception):
    pass

def listen_on(sock):
    while True:
        # get the next incoming connection
        # print "listen_on: before yield"
        yield "recv", sock
        client, addr = sock.accept()
        # We've a client now, now it's time to go and handle this client
        yield Task(echo_handler(client))

# Create a scheduler to manage all our coroutines
# Create a coroutine instance to run the echo_handler on
# incoming connections
#

def nonblocking_read(sock):
    """
    A coroutine that read's data in a non-blocking manner.
    """
    try:
        # Following read is going to be non-blocking because we
        # come here from IO loop.

        data = sock.recv(1024)

        if len(data) == 0:
            print "ConnectionLost"
            raise ConnectionLost("EOF")

        return data
    except Exception as e:
        print e


def nonblocking_write(sock, data):

    try:
        sent = 0
        sent = sock.send(data)
        if sent == 0:
            raise ConnectionLost("EOF")
    except socket.error:
        sent = -1
    finally:
        return sent

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
            print "running handler"

            yield "recv", sock
            data = nonblocking_read(sock)

            if data:
                yield "send", sock
                written = nonblocking_write(sock, data)

        except ConnectionLost:
            print "ConnectionLost"
            return
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
        return self.target.send(self.sendval)


class Scheduler(object):

    def __init__(self):
        self.taskmap = {}
        self.runqueue = collections.deque()
        self.epoll = None
        self.stopped = False

    def wait_for_io(self, why, sock, task):
        """
        We need to register interest in I/O events.
        """
        if not self.epoll:
            RuntimeError("Nothing to wait for I/O on.")

        if why in ('recv', 'send'):
            fd = sock.fileno()
            if why == 'recv':
                print("registering for I/O read:", fd)
                self.epoll.register(fd, select.EPOLLIN)
            elif why == 'send':
                print("registering for I/O write:", fd)
                self.epoll.register(fd, select.EPOLLOUT)
            self.taskmap[fd] = task

        elif why == 'task':
            self.schedule(task)


    def run(self):
        self.epoll = select.epoll()
        self.stopped = False

    def stop(self):
        self.stopped = True

    def schedule(self, task):
        if not isinstance(task, Task):
            raise ValueError("{} should be an instance of {}", task, Task)
        self.runqueue.append(task)

    def loop(self):

        while True:
            if self.stopped:
                break
            while not self.runqueue:
                # Wait for some I/O notification
                print("waiting for IO")
                events = self.epoll.poll(1)
                for fileno, event in events:
                    self.epoll.unregister(fileno)
                    task = self.taskmap.get(fileno, None)
                    if task:
                        self.runqueue.append(task)
            while self.runqueue:
                task = self.runqueue.popleft()
                print("running task:", task.target.__name__)
                result = task.run()
                if result:
                    if isinstance(result, Task):
                        self.schedule(result)
                    else:
                        why, what = result
                        # So we have something that is waiting for I/O now
                        # So we need to make sure they are polled on
                        self.wait_for_io(why, what, task)

s = Scheduler()

s.schedule(Task(server))

s.run()
s.loop()

