import os


class CsvFile:
    def __init__(self, filename):
        need_header = not os.path.isfile(filename)
        self.f = open(filename, "a")
        if need_header:
            self._write_header()
    
    def close(self):
        self.f.close()

    def append(self, data):
        self._write_value(data)

    def _write_header(self):
        self.f.write('time,cpu_temperature,outside_temperature,level\n')

    def _write_value(self, data):
        time = data['time']
        cpu_temp = str(data['cpu_temperature'])
        outside_temp = str(data['outside_temperature'])
        level = str(data['level'])
        self.f.write(time+','+cpu_temp+','+outside_temp+','+level+'\n')

