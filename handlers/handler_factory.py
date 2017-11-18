import handlers.file_handler as fh
import handlers.method_handler as mh
import logging

logger = logging.getLogger(__name__)


def get_source_handler(args):
    if not args.input:
        raise AttributeError('No input provided')
    source = args.input
    handler = fh.FileHandler(source=source)
    return handler


def get_target_handler(args):
    target = args.out
    # if not target:
    #     target = 'target'
    handler = fh.FileHandler(target=target)
    return handler


def get_method_handler(args):
    return mh.MethodHandler()
