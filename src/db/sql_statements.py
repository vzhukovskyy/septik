class SqlStatements:
    def columns(self):
        return ['time', \
                'cpu_temperature', \
                'outside_temperature', \
                'humidity', \
                'pressure', \
                'flow', \
                'level' \
                ]

    def insert(self, time, cpu_temperature, outside_temperature, humidity, pressure, flow, level):
        sql = """
            INSERT INTO sensors (
                time, 
                cpu_temperature, 
                outside_temperature, 
                humidity, 
                pressure, 
                flow, 
                level) 
            VALUES (
                  :time_column_value,
                  :cpu_temperature,
                  :outside_temperature,
                  :humidity,
                  :pressure,
                  :flow,
                  :level
            )"""

        values = { \
           'time_column_value': time, \
           'cpu_temperature': cpu_temperature, \
           'outside_temperature': outside_temperature, \
           'humidity': humidity, \
           'pressure': pressure, \
           'flow': flow, \
           'level': level \
            }

        return sql, values

    def create_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS sensors (
                  time DATETIME PRIMARY KEY,
                  cpu_temperature FLOAT,
                  outside_temperature FLOAT,
                  humidity FLOAT,
                  pressure FLOAT,
                  flow FLOAT,
                  level FLOAT)"""
        return sql

    def select_between(self, start_time, end_time):
        return """
            SELECT 
               strftime('%Y-%m-%d %H:%M:%f', time, 'localtime'), 
               cpu_temperature, 
               outside_temperature, 
               humidity, 
               pressure, 
               flow, 
               level
            FROM 
                sensors 
            WHERE 
                time BETWEEN '{start_time}' AND '{end_time}'"""\
            .format(start_time=start_time, end_time=end_time)

    def delete(self):
        return """
            DELETE FROM sensors
        """

    def drop(self):
        return """
            DROP TABLE sensors
        """
