import threading
from datetime import datetime
from latest_data import latest_data
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
            data = latest_data.get()
            if data:
                print datetime.now(), '- stored data in UTC as', str(data['time'])
                db.store(data)
            threading.Timer(1, self._timer_func).start()
