from functools import wraps
import os
import errno
import signal

from utils.timeout.exception import *


def _handle_timeout(signum, frame):
    raise KilledExecTimeout("Timeout and func was killed")


signal.signal(signal.SIGALRM, _handle_timeout)


def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def wrapper(*args, **kwargs):
            signal.setitimer(signal.ITIMER_REAL, seconds) #used timer instead of alarm
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return wraps(func)(wrapper)
    return decorator


def timeout_call(func, delay, args=None, kwargs=None):
    signal.setitimer(signal.ITIMER_REAL, float(delay)) #used timer instead of alarm
    try:
        result = func(*args, **kwargs)
    finally:
        signal.alarm(0)
    return result
