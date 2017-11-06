import handlers.bulk_text as btext


class FileHandler:

    def __init__(self, level, source):
        self.source = source


    def load_source(self):
        # self.log.debug('Loading texts from path {}.'.format(self.source))
        return btext.load(self.source)
