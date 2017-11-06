#!/usr/bin/python
# -*- coding: utf-8 -*-
import cli
import handlers.handler_factory as factory
import process
import logging
from log import configLogging

logger = logging.getLogger(__name__)


def main():
    args = cli.parse_args()
    configLogging(args)
    logger.info('STARTING...')
    source_handler = factory.get_source_handler(args)
    target_handler = factory.get_target_handler(args)
    method_handler = factory.get_method_handler(args)
    process.run(source_handler, target_handler, method_handler)


if __name__ == '__main__':
    main()
