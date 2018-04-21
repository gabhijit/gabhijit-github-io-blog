import logging

from foo.bar.baz import log
from foo.bar.baz import mod

logging.basicConfig()
l = logging.getLogger()

print "name:", __name__, "handlers:", l.handlers, "me:", l, "parent:", l.parent


log()
