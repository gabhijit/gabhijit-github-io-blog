import logging

print "root handlers:", logging.root.handlers


logging.basicConfig()

l = logging.getLogger(__name__)
l.addHandler(logging.StreamHandler())
l.setLevel(logging.INFO)

from foo.bar.baz import log
from foo.bar.baz import mod
from foo import get_log_parent, setup_logging

print "name:", __name__, "handlers:", l.handlers, "me:", l, "parent:", l.parent

print "foo package Logger Parent:", get_log_parent()
print "foo package Logger Parent handlers:", get_log_parent().handlers

setup_logging(logging.StreamHandler())

log()
