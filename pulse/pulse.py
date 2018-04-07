import sys, time, os, threading, BaseHTTPServer
from datetime import datetime

statistics = Statistics()


def jsonify(adict):
    s = '{'
    first = True
    for key,value in adict.iteritems():
        if first:
            first = False
        else:
            s += ',' 
        s += '"'+key+'"' + ':' + str(value)
    s += '}'
    return s

class CsvFile:
    def __init__(self, filename):
        self.f = self._open(filename)
        self.header_written = False
    
    def close(self):
        self.f.close()

    def append(self, stat):
        if not self.header_written:
            self._write_header(stat)
            self.header_written = True
        self._write_value(stat)

    def _write_header(self, stat):
        self.f.write('date,cpu,mem\n')

    def _write_value(self, stat):
        date = stat['date']
        cpu = str(stat['cpu'])
        mem = str(stat['mem'])
        self.f.write(date+','+cpu+','+mem+'\n')

    def _open(self, filename):
        try:
            stat_info = os.stat(filename)
            filetime = datetime.fromtimestamp(stat_info.st_ctime)
            os.rename(filename, filename+"."+str(filetime))
        except OSError:
            pass
        f = open(filename, "w")
        return f

class StatisticsLogger:
    def start(self):
        self.csvfile = CsvFile('pulse.csv')
        self.exiting = False
        threading.Timer(1, self._timer_func).start()

    def stop(self):
        self.exiting = True
        self.csvfile.close()

    def _timer_func(self):
        if not self.exiting:
            stat = statistics.get()
            print threading.currentThread(),'StatisticsLogger:',stat
            self.csvfile.append(stat)
            threading.Timer(1, self._timer_func).start()

