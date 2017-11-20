import os
from logging import getLogger

from . import bulk_text as btext


class FileHandler:
    logger = getLogger(__name__)

    def __init__(self, source=None, target=None):
        self.source = source
        self.target = target

    def load(self):
        self.logger.debug('Loading texts from {}'.format(self.source))
        return btext.load(self.source)

    def save(self, filename, text):
        path = os.path.join(self.target, filename)
        self.logger.debug('Saving text to {}'.format(path))
        btext.save(path, text)
