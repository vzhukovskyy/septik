import sqlite3
import threading
from sql_statements import SqlStatements


class Db:
    def __init__(self):
        self._lock = threading.Lock()

        self.sqlStatements = SqlStatements()
        self.conn = sqlite3.connect('db.sqlite', check_same_thread = False)
        self.cursor = self.conn.cursor()
        self._create()

    def store(self, sensor_data):
        self._lock.acquire()

        sql, values = self.sqlStatements.insert(time=sensor_data['time'], \
                                                cpu_temperature=sensor_data['cpu_temperature'], \
                                                outside_temperature = sensor_data['outside_temperature'], \
                                                flow=sensor_data['flow'], \
                                                level=sensor_data['level'])
        with self.conn:
            self.cursor.execute(sql, values)

        self._lock.release()

    def get_latest(self, start_time):
        self._lock.acquire()

        sql = self.sqlStatements.select_since(start_time)
        self.cursor.execute(sql)
        records = self.cursor.fetchall()

        self._lock.release()
        return records

    def _create(self):
        try:
            self.cursor.execute(self.sqlStatements.create_table())
        except sqlite3.OperationalError:
            # db already exists - ignore it
            pass

    def close(self):
        self.conn.close()
