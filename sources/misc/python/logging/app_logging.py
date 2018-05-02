from foo.bar.baz import log
from foo.bar.baz import mod

from foo import get_log_parent


import logging

print "root handlers:", logging.root.handlers

# logging.basicConfig()

l = logging.getLogger('app')
l.addHandler(logging.StreamHandler())

print "name:", __name__, "handlers:", l.handlers, "me:", l, "parent:", l.parent


print "foo package Logger Parent:", get_log_parent()
print "foo package Logger Parent handlers:", get_log_parent().handlers
log()
