import threading
from latest_data import latestData
from src.db.db import db


class DataLogger:
    def __init__(self):
        self.exiting = False

    def start(self):
        threading.Timer(1, self._timer_func).start()

    def stop(self):
        self.exiting = True
        db.close()

    def _timer_func(self):
        if not self.exiting:
            data = latestData.get()
            #print(threading.currentThread(),'DataLogger:',data)
            if data:
                db.store(data)
            threading.Timer(1, self._timer_func).start()
