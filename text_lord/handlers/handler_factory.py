import logging
from urllib.parse import urlparse

from .method_handler import MethodHandler
from .file_handler import FileHandler
from .target_strategy import TargetStrategy

logger = logging.getLogger(__name__)


def get_source_handler(args):
    if not args.input:
        raise AttributeError('No input provided')
    source = args.input
    handler = FileHandler(source=source)
    return handler


def get_target_handler(args):
    save_handler = out_save_handler(args)
    separate = args.separate
    tree = args.tree
    origin_source = args.input
    target_strategy = TargetStrategy(save_handler, origin_source, tree,
                                     separate)
    return target_strategy


def get_method_handler(args):
    methods = []
    if args.textrank:
        methods.append('textrank')
    if args.lexrank:
        methods.append('lexrank')
    return MethodHandler(methods)


def out_save_handler(args):
    out_url = urlparse(args.out)
    if not out_url.path:
        target = None
        return FileHandler(target=target)
    if not out_url.sheme:
        target = out_url.path
        return FileHandler(target=target)
