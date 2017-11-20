from logging import getLogger

from text_lord.algorithms import textrank


class MethodHandler:
    logger = getLogger(__name__)

    def __init__(self, methods):
        self.methods = methods

    def extract(self, text, n=5):
        if self.methods.count('textrank') > 0:
            self.logger.debug('Extracting summary size of {} with TextRank'
                              .format(n))
            return textrank.extract(text, n)
        else:
            return textrank.extract(text, n)

    def get_method(self):
        return textrank
