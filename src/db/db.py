import sqlite3
import threading
from sql_statements import SqlStatements


class Db:
    def __init__(self):
        self._lock = threading.Lock()
        self.sqlStatements = SqlStatements()
        self._open()

    def _open(self):
        self.conn = sqlite3.connect('data/db.sqlite', check_same_thread = False)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        with self._lock:
            self.cursor.execute(self.sqlStatements.create_table())

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def store(self, sensor_data, commit=True):
        with self._lock:
            sql, values = self.sqlStatements.insert(time=sensor_data['time'], \
                                                    cpu_temperature=sensor_data['cpu_temperature'], \
                                                    outside_temperature = sensor_data['outside_temperature'], \
                                                    humidity=sensor_data['humidity'], \
                                                    pressure=sensor_data['pressure'], \
                                                    flow=sensor_data['flow'], \
                                                    level=sensor_data['level'])
            try:
                self.cursor.execute(sql, values)
            except sqlite3.IntegrityError:
                return False

            if commit:
               self.conn.commit()
        return True

    def commit(self):
        self.conn.commit()

    def query(self, start_time, end_time):
        with self._lock:
            sql = self.sqlStatements.select_between(start_time, end_time)
            self.cursor.execute(sql)
            records = self.cursor.fetchall()
            return records

    def transpose(self, records):
        series = [[r[col] for r in records] for col in range(len(records[0]))]
        columns = self.columns()
        data = {columns[i]:series[i] for i in range(len(columns))}
        return data

    def columns(self):
        return self.sqlStatements.columns()

    def close(self):
        self.conn.close()

    def drop(self):
        with self._lock:
            self.cursor.execute(self.sqlStatements.delete())
            self.cursor.execute(self.sqlStatements.drop())
            self.conn.commit()


db = Db()
