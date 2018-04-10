import threading
from csv_file import CsvFile
from latest_data import latestData


class DataLogger:
    def __init__(self):
        self.csv_file = CsvFile('pulse.csv')
        self.exiting = False

    def start(self):
        threading.Timer(1, self._timer_func).start()

    def stop(self):
        self.exiting = True
        self.csv_file.close()

    def _timer_func(self):
        if not self.exiting:
            data = latestData.get()
            #print(threading.currentThread(),'DataLogger:',data)
            self.csv_file.append(data)
            threading.Timer(1, self._timer_func).start()
