import logging

l = logging.getLogger(__name__)
print "name:", __name__, "handlers:", l.handlers, "me:", l, "parent:", l.parent

# Following won't get printed during import (as the RootLogger's handler is NullHandler)
l.warning("hi from baz")


def log():
    # Following will be printed, if called after logger in application is setup with proper handler (say StreamHandler)
    l.warning("hi again from baz")
