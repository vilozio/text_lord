import logging

from .method_handler import MethodHandler
from .file_handler import FileHandler

logger = logging.getLogger(__name__)


def get_source_handler(args):
    if not args.input:
        raise AttributeError('No input provided')
    source = args.input
    handler = FileHandler(source=source)
    return handler


def get_target_handler(args):
    target = args.out
    # if not target:
    #     target = 'target'
    handler = FileHandler(target=target)
    return handler


def get_method_handler(args):
    methods = []
    if args.textrank:
        methods.append('textrank')
    return MethodHandler(methods)