# This is a working implementation of coroutine based echo server as
# suggested in Pep 342

# One major problem with this is 'run' method does a 'busy polling' and
# That's generally bad.

# FIXME: To make it into select or epoll to avoid 'busy polling'

import collections
import socket
import types
import sys

class ConnectionLost(Exception):
    pass

class Trampoline:
    """Manage communications between coroutines"""

    running = False

    def __init__(self):
        self.queue = collections.deque()

    def add(self, coroutine):
        """Request that a coroutine be executed"""
        self.schedule(coroutine)

    def run(self):
        result = None
        self.running = True
        try:
            while self.running and self.queue:
                try:
                    func = self.queue.popleft()
                    result = func()
                except StopIteration:
                    print "StopIteration"
                except Exception as e:
                    print e
            return result
        finally:
            self.running = False

    def stop(self):
        self.running = False

    def schedule(self, coroutine, stack=(), val=None, *exc):
        def resume():
            print "coroutine is:", coroutine.__name__
            value = val
            try:
                if exc:
                    value = coroutine.throw(value,*exc)
                else:
                    print coroutine.__name__, ".send(", value, ")"
                    value = coroutine.send(value)
            except:
                if stack:
                    # send the error back to the "caller"
                    self.schedule(
                        stack[0], stack[1], *sys.exc_info()
                    )
                else:
                    # Nothing left in this pseudothread to
                    # handle it, let it propagate to the
                    # run loop
                    raise

            if isinstance(value, types.GeneratorType):
                print "value:", value
                # Yielded to a specific coroutine, push the
                # current one on the stack, and call the new
                # one with no args
                self.schedule(value, (coroutine,stack))

            elif stack:
                print "stack:", stack
                # Yielded a result, pop the stack and send the
                # value to the caller
                self.schedule(stack[0], stack[1], value)

            # else: this pseudothread has ended

        self.queue.append(resume)
        print self.queue

# A simple echo server, and code to run it using a trampoline
# (presumes the existence of nonblocking_read, nonblocking_write,
# and other I/O coroutines, that e.g. raise ConnectionLost if the
# connection is closed):

# coroutine function that echos data back on a connected
# socket
#
def echo_handler(sock):
    print sock
    while True:
        try:
            data = yield nonblocking_read(sock)
            print "*****Received Data*****:", "".join(data)
            if data:
                yield nonblocking_write(sock, data)
        except ConnectionLost:
            break
            #pass  # exit normally if connection lost

# coroutine function that listens for connections on a
# socket, and then launches a service "handler" coroutine
# to service the connection
#
def listen_on(trampoline, sock, handler):
    while True:
        # get the next incoming connection
        print "listen_on: before yield"
        connected_socket = yield nonblocking_accept(sock)
        print "connected_socket", connected_socket

        # start another coroutine to handle the connection
        if connected_socket > 0:
            trampoline.add(handler(connected_socket))

# Create a scheduler to manage all our coroutines
t = Trampoline()

# Create a coroutine instance to run the echo_handler on
# incoming connections
#

def nonblocking_read(sock):
    """
    A coroutine that read's data in a non-blocking manner.
    """
    try:
        data = sock.recv(1024)

        if len(data) == 0:
            raise ConnectionLost("EOF")

        yield data

    except socket.error:
        # EWOULDBLOCK we return empty data,
        yield []


def nonblocking_write(sock, data):

    try:
        sent = sock.send(data)
        if sent == 0:
            raise ConnectionLost("EOF")
    except socket.error:
        sent = -1
    finally:
        yield sent

def nonblocking_accept(sock):

    print "nonblocking_accept being called."
    try:
        value, _ = sock.accept()
        value.setblocking(False)
    except socket.error as e:
        value = -1
    finally:
        yield value

def listening_socket(host, port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)
    sock.setblocking(False)

    return sock

server = listen_on(
    t, listening_socket("localhost",7777), echo_handler
)

# Add the coroutine to the scheduler
t.add(server)

# loop forever, accepting connections and servicing them
# "in parallel"
#
t.run()

"""
Let's reason about this code

When 'listen_on' is added to the Trampoline at `t.add(server)`
`t.schedule(listen_on) get's called. This is going to first do a
listen_on.send(None) in the schedule and bring it to a point where it `yield`s
for the first time. ie. `yield nonblocking_accept(sock)` so the value
is now nonblocking_accept - coroutine object and that's added

and `t.run()` is run -
"""
