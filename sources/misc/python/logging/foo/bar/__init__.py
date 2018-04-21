import logging


l = logging.getLogger(__name__)
print "name:", __name__, "handlers:", l.handlers, "me:", l, "parent:", l.parent

l.warning("hi there")
