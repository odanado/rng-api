import logging
from bottle import request, response
from functools import wraps
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger('rngapi')

# set up the logger
logger.setLevel(logging.INFO)
# file_handler = logging.FileHandler('logs/rngapi.log')
file_handler = TimedRotatingFileHandler('logs/access.log', 'd', 7)
formatter = logging.Formatter('%(msg)s')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def log_to_logger(fn):
    '''
    Wrap a Bottle request so that a log line is emitted after it's handled.
    (This decorator can be extended to take the desired logger as a param.)
    '''
    @wraps(fn)
    def _log_to_logger(*args, **kwargs):
        request_time = datetime.now()
        actual_response = fn(*args, **kwargs)
        # modify this to log exactly what you need:
        logger.info('%s %s %s %s %s' % (request.remote_addr,
                                        request_time,
                                        request.method,
                                        request.url,
                                        response.status))
        return actual_response
    return _log_to_logger
