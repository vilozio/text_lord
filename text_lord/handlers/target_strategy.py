import os
import logging

logger = logging.getLogger(__name__)


class TargetStrategy:
    def __init__(self, save_handler, origin_source, tree, separate):
        self.save_handler = save_handler
        self.origin_source = origin_source
        self.tree = tree
        self.separate = separate
        self.file_suffix = ''

    def preprocess(self, origin_path, method_name):
        dirs, filename = os.path.split(origin_path)
        if self.tree:
            if self.separate:
                self.save_handler.target = target_relative_to_source(
                    self.origin_source, 'target')
                filename = os.path.join(dirs[len(origin_path):],
                                        filename)
            else:
                self.save_handler.target = dirs
        if method_name == 'textrank': self.file_suffix = '.tr'
        if method_name == 'lexrank': self.file_suffix = '.lr'

    def save(self, text, origin_path):
        dirs, filename = os.path.split(origin_path)

        filename = filename + self.file_suffix
        self.save_handler.save(filename, text)


def target_relative_to_source(original_source, target):
    source = original_source
    source = source[:-1] if source.endswith('/') else source
    source_path, source_dir = os.path.split(source)
    new_target_dir = target + '_' + source_dir
    new_target = os.path.join(source_path, new_target_dir)
    return new_target
