from datetime import datetime


class Logger:
    CLASS_HTTP = 'HTTP'
    CLASS_DB = 'DB'
    CLASS_AGGREGATOR = 'AGG'

    def log(self, cls, message):
        if self._filter(cls):
            print datetime.now().strftime("%Y-%m-%d %H:%M:%S"), cls, message

    def _filter(self, cls):
        if cls != self.CLASS_DB:
            return True
        return False


logger = Logger()
