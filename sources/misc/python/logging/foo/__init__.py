
import logging

print logging.root


l  = logging.getLogger(__name__)
l.addHandler(logging.NullHandler())

print "name:", __name__, "handlers:", l.handlers, "me:", l, "parent:", l.parent


def get_log_parent():
    return l.parent


def setup_logging(handler):

    print "before 1"
    fmt = '%(name)40s : %(asctime)s : %(message)s'
    l.addHandler(handler)
    print "after 1"
    handler.setFormatter(logging.Formatter(fmt))
    print "after 2"
