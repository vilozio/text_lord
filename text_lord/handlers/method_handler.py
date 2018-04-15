from logging import getLogger

from text_lord.algorithms import textrank
from text_lord.algorithms import lexrank
from text_lord.algorithms.vsm import cosine, normalize_by_length


class MethodHandler:
    logger = getLogger(__name__)

    def __init__(self, methods):
        self.methods = methods
        self.source_handler = None
        self.target_handler = None

    # def extract(self, text, n=5):
    #     if self.methods.count('textrank') > 0:
    #         self.logger.debug('Extracting summary size of {} with TextRank'
    #                           .format(n))
    #         return textrank.extract(text, n)
    #     # else:
    #     #     lr = lexrank.LexRank('./datasets/bbc', 'txt')
    #     #     lr.multiDocSummarization(cosine,
    #     #                               normalizeByLength)
    #     #     return lr.rank(0.1, 0.005, 100, True, 0.15, True)

    def set_state(self, source_handler, target_handler):
        self.source_handler = source_handler
        self.target_handler = target_handler

    def extract(self, n=5):
        texts = self.source_handler.load()
        if self.methods.count('textrank') > 0:
            for path, text in texts.items():
                self.logger.debug('Extracting textrank summary for {0}'.format(
                    path))
                summary = textrank.extract(text, n)
                self.target_handler.preprocess(path, 'textrank')
                self.target_handler.save(summary, path)
        if self.methods.count('lexrank') > 0:
            self.logger.debug('Extracting lexrank')
            lr = lexrank.LexRank(texts)
            lr.summarization(cosine, normalize_by_length)
            rankings, sentences = lr.rank(0.1, 0.005, 100, True, 0.15)
            self.logger.debug('{0}\n {1}'.format(rankings, sentences))


# def get_method(self):
#     return textrank
