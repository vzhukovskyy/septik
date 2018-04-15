class SqlStatements:
    def __init__(self):
        self.sqlite_file = 'db.sqlite'
        self.table_name = 'sensors'
        self.time_column = ('time', 'DATETIME')
        self.cpu_temperature_column = ('cpu_temperature', 'FLOAT')
        self.outside_temperature_column = ('outside_temperature', 'FLOAT')
        self.humidity_column = ('humidity', 'FLOAT')
        self.pressure_column = ('pressure', 'FLOAT')
        self.flow_column = ('flow', 'FLOAT')
        self.level_column = ('level', 'FLOAT')

    def columns(self):
        return [self.time_column[0], \
                self.cpu_temperature_column[0], \
                self.outside_temperature_column[0], \
                self.humidity_column[0], \
                self.pressure_column[0], \
                self.flow_column[0], \
                self.level_column[0] \
                ]

    def insert(self, time, cpu_temperature, outside_temperature, humidity, pressure, flow, level):
        sql = """
            INSERT INTO {table} (
                {time_column_name}, 
                {cpu_temperature_column_name}, 
                {outside_temperature_column_name}, 
                {humidity_column_name}, 
                {pressure_column_name}, 
                {flow_column_name}, 
                {level_column_name}) 
            VALUES (
                  :time_column_value,
                  :cpu_temperature,
                  :outside_temperature,
                  :humidity,
                  :pressure,
                  :flow,
                  :level
            )""".format(
                table=self.table_name, \
                time_column_name=self.time_column[0], \
                cpu_temperature_column_name=self.cpu_temperature_column[0], \
                outside_temperature_column_name=self.outside_temperature_column[0], \
                humidity_column_name=self.humidity_column[0], \
                pressure_column_name=self.pressure_column[0], \
                flow_column_name=self.flow_column[0], \
                level_column_name=self.level_column[0])

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
            CREATE TABLE IF NOT EXISTS {table} (
                  {time_column_name} {time_column_type} PRIMARY KEY,
                  {cpu_temperature_column_name} {cpu_temperature_column_type},
                  {outside_temperature_column_name} {outside_temperature_column_column_type},
                  {humidity_column_name} {humidity_column_column_type},
                  {pressure_column_name} {pressure_column_column_type},
                  {flow_column_name} {flow_column_type},
                  {level_column_name} {level_column_type})
                  """.format(table=self.table_name, \
                             time_column_name=self.time_column[0], \
                             time_column_type=self.time_column[1], \
                             cpu_temperature_column_name=self.cpu_temperature_column[0], \
                             cpu_temperature_column_type=self.cpu_temperature_column[1], \
                             outside_temperature_column_name=self.outside_temperature_column[0], \
                             outside_temperature_column_column_type=self.outside_temperature_column[1], \
                             humidity_column_name=self.humidity_column[0], \
                             humidity_column_column_type=self.humidity_column[1], \
                             pressure_column_name=self.pressure_column[0], \
                             pressure_column_column_type=self.pressure_column[1], \
                             flow_column_name=self.flow_column[0], \
                             flow_column_type=self.flow_column[1], \
                             level_column_name=self.level_column[0], \
                             level_column_type=self.level_column[1] \
                             )
        return sql

    def select_all(self):
        return """
            SELECT * FROM {table}
        """.format(table=self.table_name)

    def select_between(self, start_time, end_time):
        return "SELECT * FROM {table} WHERE {time_column_name} BETWEEN '{start_time}' AND '{end_time}'"\
            .format(table=self.table_name, \
                    time_column_name=self.time_column[0], \
                    start_time=start_time, \
                    end_time=end_time)

    def select_since(self, start_time):
        return "SELECT * FROM {table} WHERE {time_column_name} >= '{start_time}'"\
            .format(table=self.table_name, \
                    time_column_name=self.time_column[0], \
                    start_time=start_time)

    def delete(self):
        return """
            DELETE FROM {table}
        """.format(table=self.table_name)

    def drop(self):
        return """
            DROP TABLE {table}
        """.format(table=self.table_name)
