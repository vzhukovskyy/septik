import threading


class LatestData:
    def __init__(self):
        self._data = None
        self._lock = threading.Lock()

    def get(self):
        self._lock.acquire()
        if self._data is None:
            s = None
        else:
            s = dict(self._data)
        self._lock.release()
        return s
    
    def set(self, s):
        self._lock.acquire()
        self._data = s
        self._lock.release()

latestData = LatestData()
