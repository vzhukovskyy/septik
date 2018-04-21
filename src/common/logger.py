from datetime import datetime

class Logger:
    CLASS_HTTP = 'HTTP'
    CLASS_DB = 'DB'

    def log(self, cls, message):
        if self._filter(cls):
            print datetime.now(), message

    def _filter(self, cls):
        if cls == self.CLASS_HTTP:
            return True
        return False

logger = Logger()