from datetime import datetime


class Sensors:
    def __init__(self):
        pass

    def get_data(self):
        return self._get_simulated_data()

    def _get_simulated_data(self):
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cpu_temp = 30
        outside_temp = 10
        pressure = 980
        humidity = 98
        flow = 9
        level = 85

        ret = {
            'time': time,
            'cpu_temperature': cpu_temp,
            'outside_temperature': outside_temp,
            'pressure': pressure,
            'humidity': humidity,
            'flow': flow,
            'level': level
        }
        return ret


sensors = Sensors()