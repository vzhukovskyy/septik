from src.utils.timeutil import timeutil

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

    def insert(self, table, time, cpu_temperature, outside_temperature, humidity, pressure, flow, level):
        sql = """
            INSERT INTO {name} (
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
            )"""\
            .format(name=table)

        values = { \
           'time_column_value': timeutil.to_db_time(time), \
           'cpu_temperature': cpu_temperature, \
           'outside_temperature': outside_temperature, \
           'humidity': humidity, \
           'pressure': pressure, \
           'flow': flow, \
           'level': level \
            }

        return sql, values

    def create_table(self, table_name):
        sql = """
            CREATE TABLE IF NOT EXISTS {name} (
                  time DATETIME PRIMARY KEY,
                  cpu_temperature FLOAT,
                  outside_temperature FLOAT,
                  humidity FLOAT,
                  pressure FLOAT,
                  flow FLOAT,
                  level FLOAT)""".format(name=table_name)
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
            .format(start_time=timeutil.to_db_time(start_time), end_time=timeutil.to_db_time(end_time))

    def select_latest(self, table_name):
        return """
            SELECT 
               strftime('%Y-%m-%d %H:%M:%f', time, 'localtime')
            FROM 
                {name} t
            INNER JOIN (SELECT max(time) AS max_time FROM {name}) max_t ON t.time=max_t.max_time
            """\
            .format(name=table_name)

    def select_earliest(self, table_name):
        return """
            SELECT 
               strftime('%Y-%m-%d %H:%M:%f', time, 'localtime')
            FROM 
                {name} t
            INNER JOIN 
                (SELECT min(time) AS min_time FROM {name} WHERE length(time)>0) min_t 
            ON
                t.time = min_t.min_time
            """\
            .format(name=table_name)

    def delete(self, table):
        return """
            DELETE FROM {table}
        """.format(table=table)

    def drop(self, table):
        return """
            DROP TABLE {table}
        """.format(table=table)
