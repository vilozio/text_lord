import os
import logging

logger = logging.getLogger(__name__)


def run(source_handler, target_handler, method_handler, args):
    texts = source_handler.load()
    target = target_handler.target
    for path, text in texts.items():
        logger.debug('Extracting summary for {0}'.format(path))
        summary = method_handler.get_method().extract(text, 1)
        # logger.debug('Result summary for {0}: {1}'.format(path, summary))
        dirs, filename = os.path.split(path)

        if args.tree:
            if target:
                source = source_handler.source.replace('/', '')
                new_target_dir = target + '_' + source
                new_target = dirs.replace(source, new_target_dir, 1)
                target_handler.target = new_target
            else:
                target_handler.target = dirs
                filename = filename + '.tr'
        target_handler.save(filename, summary)
