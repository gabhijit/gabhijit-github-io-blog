import logging
import time

import profiler

iterations = 1000000
l = logging.getLogger(__name__)
l.addHandler(logging.NullHandler())

l.setLevel(logging.INFO)

class Foo(object):
    def __str__(self):
        return "%s" % self.__class__

with profiler.Profiler(enabled=True, contextstr="non lazy logging") as p:
    for i in range(iterations):
        l.debug("Hello There. %s" % Foo())

p.print_profile_data()

then = time.time()

with profiler.Profiler(enabled=True, contextstr="lazy logging") as p:
    for i in range(iterations):
        l.debug("Hello There. %s", Foo())
p.print_profile_data()

now = time.time()

lazy = now - then


