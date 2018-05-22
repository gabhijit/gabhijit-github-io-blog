import logging

import profiler

iterations = 1000
l = logging.getLogger(__name__)
l.addHandler(logging.NullHandler())

l.setLevel(logging.INFO)
l.disabled = True

with profiler.Profiler(enabled=True, contextstr="lazy logging") as p:
    for i in range(iterations):
        l.info("Hello There.")
p.print_profile_data()

