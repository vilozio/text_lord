# original author: Paul McGuire
import atexit
from time import time
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


def secondsToStr(elapsed):
    return str(timedelta(seconds=elapsed))


def endlog():
    end = time()
    elapsed = end - start
    logger.info('Completed in {0}'.format(secondsToStr(elapsed)))


# def markStart():
#     global start
#     start = time()
#     atexit.register(endlog)

start = time()
atexit.register(endlog)
