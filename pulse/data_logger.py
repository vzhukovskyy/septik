import threading
from latest_data import latestData
from db.db import Db


class DataLogger:
    def __init__(self):
        self.db = Db()
        self.exiting = False

    def start(self):
        threading.Timer(1, self._timer_func).start()

    def stop(self):
        self.exiting = True
        self.db.close()

    def _timer_func(self):
        if not self.exiting:
            data = latestData.get()
            #print(threading.currentThread(),'DataLogger:',data)
            self.db.store(data)
            threading.Timer(1, self._timer_func).start()
