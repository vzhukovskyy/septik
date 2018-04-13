import threading
from src.sensors.sensors import get_data
from latest_data import latestData


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
        latestData.set(data)
        #print(threading.currentThread(),'DataPuller:',data)
        self._schedule_next_call()
