import handlers.file_handler as fh
import handlers.method_handler as mh
import logging

logger = logging.getLogger(__name__)
logger2 = logging.getLogger('handler_factory2')


def get_source_handler(args):
    level = 'info'
    logger.debug('SERIOUS LOGGING')
    logger2.debug('YES YES YES')
    source = args.input
    handler = fh.FileHandler(level, source)
    return handler


def get_target_handler(args):
    level = 'info'
    source = args.out
    handler = fh.FileHandler(level, source)
    return handler

def get_method_handler(args):
    return mh.get_method()
