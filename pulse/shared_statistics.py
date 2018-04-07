class SharedStatistics:
    def __init__(self):
        self._statistics = None
        self._lock = threading.Lock()

    def get(self):
        self._lock.acquire()
        if self._statistics is None:
            s = None
        else:
            s = dict(self._statistics)
        self._lock.release()
        return s
    
    def set(self, s):
        self._lock.acquire()
        self._statistics = s
        self._lock.release()
