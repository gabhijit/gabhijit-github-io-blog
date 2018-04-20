import logging

from foo.bar.baz import log

logging.basicConfig()
l = logging.getLogger()

print __name__, l.handlers, l, l.parent


log()
