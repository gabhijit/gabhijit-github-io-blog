
import logging

fmt = '%(name)40s : %(asctime)s : %(message)s'

module_logger  = logging.getLogger(__name__)
module_logger.addHandler(logging.NullHandler())

print __name__, module_logger.handlers, module_logger, module_logger.parent

