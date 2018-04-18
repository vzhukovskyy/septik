import threading
from src.sensors.sensors import get_data
from latest_data import latest_data, latest_filtered_data
from src.analyzer.filter import data_filter


class DataPuller:
    def __init__(self):
        self._timer = None
        self._lock = threading.Lock()

    def start(self):
        self._schedule_next_call()
    
    def stop(self):
        self._cancel_next_call()

    def _cancel_next_call(self):
        self._lock.acquire()
        self._timer.cancel()
        self._lock.release()

    def _schedule_next_call(self):
        self._lock.acquire()
        self._timer = threading.Timer(1, self._timer_func)
        self._timer.start()
        self._lock.release()

    def _timer_func(self):
        data = get_data()
        filtered_data = data_filter.filter_value(data, latest_filtered_data.get())

        latest_data.set(data)
        latest_filtered_data.set(filtered_data)
        # print 'DataPuller'
        # print data
        # print filtered_data
        self._schedule_next_call()
