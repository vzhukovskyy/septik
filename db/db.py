import sqlite3
import threading
from sql_statements import SqlStatements


class Db:
    def __init__(self):
        self._lock = threading.Lock()
        self.sqlStatements = SqlStatements()
        self._open()

    def _open(self):
        self.conn = sqlite3.connect('../db/db.sqlite', check_same_thread = False)
        self.cursor = self.conn.cursor()
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

    def get_latest(self, start_time):
        with self._lock:
            sql = self.sqlStatements.select_since(start_time)
            self.cursor.execute(sql)
            records = self.cursor.fetchall()
            return records

    def close(self):
        self.conn.close()

    def empty(self):
        self.cursor.execute(self.sqlStatements.delete())
        self.conn.commit()
