import logging, time 
import logging.handlers as handlers
from datetime import datetime

class Logger:
    CLASS_HTTP = 'HTTP'
    CLASS_DB = 'DB'
    CLASS_AGGREGATOR = 'AGG'

    def __init__(self):
        self.file_logger = logging.getLogger('septik')
        self.file_logger.setLevel(logging.INFO)

        logHandler = handlers.RotatingFileHandler('messages.log', maxBytes=1*1024*1024, backupCount=2)
        logHandler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s %(message)s')
        logHandler.setFormatter(formatter)

        self.file_logger.addHandler(logHandler)

    def log(self, cls, message):
        if self._filter(cls):
            print datetime.now().strftime("%Y-%m-%d %H:%M:%S"), cls, message
            self.file_logger.info("%s %s" % (cls, message))

    def _filter(self, cls):
        if cls != self.CLASS_DB:
            return True
        return False


logger = Logger()
