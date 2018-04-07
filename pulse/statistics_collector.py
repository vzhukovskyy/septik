class StatisticsCollector:
    def __init__(self):
        self._timer = None
        self._lock = threading.Lock()

    def start(self):
        self._schedule_next_call()
    
    def stop(self):
        self._cancel_next_call()

    def _get_statistics(self):
        cpu_percent = psutil.cpu_percent(interval=None)
        virt = psutil.virtual_memory()
        mem_usage_percent = round(float(virt.total-virt.available)/virt.total*100)
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ret = {
            'cpu': cpu_percent,
            'mem': mem_usage_percent,
            'date': '"'+date+'"'
        }
        return ret

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
        statistics.set(self._get_statistics())
        #print threading.currentThread(),'StatisticsCollector:',statistics.get()
        self._schedule_next_call()
