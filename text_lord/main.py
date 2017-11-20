import logging

from . import cli, process
from .log import configLogging
from .handlers import handler_factory as factory

logger = logging.getLogger(__name__)


def main():
    args = cli.parse_args()
    configLogging(args)
    logger.info('Starting text_lord')
    source_handler = factory.get_source_handler(args)
    target_handler = factory.get_target_handler(args)
    method_handler = factory.get_method_handler(args)
    process.run(source_handler, target_handler, method_handler, args)
