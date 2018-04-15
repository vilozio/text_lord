import os
import logging

logger = logging.getLogger(__name__)


# def run(source_handler, target_handler, method_handler, args):
#     texts = source_handler.load()
#     target = target_handler.target
#     for path, text in texts.items():
#         logger.debug('Extracting summary for {0}'.format(path))
#         summary = method_handler.extract(text, 5)
#         dirs, filename = os.path.split(path)
#
#         if args.tree:
#             if args.separate:
#                 target_handler.target = target_relative_to_source(
#                     source_handler.source, 'target')
#                 filename = os.path.join(dirs[len(source_handler.source):],
#                                         filename)
#             else:
#                 target_handler.target = dirs
#                 filename = filename + '.tr'
#         target_handler.save(filename, summary)


def run(source_handler, target_handler, method_handler, args):
    method_handler.set_state(source_handler, target_handler)
    method_handler.extract()

def target_relative_to_source(original_source, target):
    source = original_source
    source = source[:-1] if source.endswith('/') else source
    source_path, source_dir = os.path.split(source)
    new_target_dir = target + '_' + source_dir
    new_target = os.path.join(source_path, new_target_dir)
    return new_target
