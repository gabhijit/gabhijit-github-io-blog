import logging

module_logger = logging.getLogger(__name__)
print __name__, module_logger.handlers, module_logger, module_logger.parent

module_logger.warning("hi from baz")

def log():
    module_logger.warning("hi again from baz")
