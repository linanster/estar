from functools import wraps
from flask import request

from mylogger import logger

def viewfunclog(func):
    @wraps(func)
    def inner(*args, **kargs):
        logger.info('{} {}'.format(request.method, request.url))
        return func(*args, **kargs)
    return inner

