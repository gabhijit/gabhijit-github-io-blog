
import logging

print logging.root

fmt = '%(name)40s : %(asctime)s : %(message)s'

l  = logging.getLogger(__name__)
l.addHandler(logging.NullHandler())

print "name:", __name__, "handlers:", l.handlers, "me:", l, "parent:", l.parent


def get_log_parent():
    return l.parent
