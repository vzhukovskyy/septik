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
            self.cursor.execute(self.sqlStatements.create_table('sensors'))
            self.cursor.execute(self.sqlStatements.create_table('hours'))
            self.cursor.execute(self.sqlStatements.create_table('days'))

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def store(self, table_name, sensor_data, commit=True):
        with self._lock:
            sql, values = self.sqlStatements.insert(table=table_name,
                                                    time=sensor_data['time'],
                                                    cpu_temperature=sensor_data['cpu_temperature'],
                                                    outside_temperature=sensor_data['outside_temperature'],
                                                    humidity=sensor_data['humidity'],
                                                    pressure=sensor_data['pressure'],
                                                    flow=sensor_data['flow'],
                                                    level=sensor_data['level'])
            try:
                self.cursor.execute(sql, values)
            except sqlite3.IntegrityError:
                return False

            if commit:
                self.conn.commit()
        return True

    def insert(self, table_name, sensor_data, commit=True):
        with self._lock:
            sql, values = self.sqlStatements.insert(table=table_name,
                                                    time=sensor_data[0],
                                                    cpu_temperature=sensor_data[1],
                                                    outside_temperature=sensor_data[2],
                                                    humidity=sensor_data[3],
                                                    pressure=sensor_data[4],
                                                    flow=sensor_data[5],
                                                    level=sensor_data[6])
            try:
                self.cursor.execute(sql, values)
            except sqlite3.IntegrityError:
                return False

            if commit:
                self.conn.commit()
        return True

    def commit(self):
        self.conn.commit()

    def select_between(self, table, start_time, end_time):
        with self._lock:
            sql = self.sqlStatements.select_between(table, start_time, end_time)
            self.cursor.execute(sql)
            records = self.cursor.fetchall()
            return records

    def select_latest(self, table_name):
        with self._lock:
            sql = self.sqlStatements.select_latest(table_name)
            self.cursor.execute(sql)
            records = self.cursor.fetchone()
            return records

    def select_earliest(self, table_name):
        with self._lock:
            sql = self.sqlStatements.select_earliest(table_name)
            self.cursor.execute(sql)
            records = self.cursor.fetchone()
            return records

    def transpose(self, records):
        columns = self.columns()

        if len(records) == 0:
            return {columns[i]: None for i in range(len(columns))}

        series = [[r[col] for r in records] for col in range(len(records[0]))]
        data = {columns[i]:series[i] for i in range(len(columns))}
        return data

    def columns(self):
        return self.sqlStatements.columns()

    def close(self):
        self.conn.close()

    def drop(self):
        with self._lock:
            self.cursor.execute(self.sqlStatements.delete('sensors'))
            self.cursor.execute(self.sqlStatements.delete('hours'))
            self.cursor.execute(self.sqlStatements.drop('sensors'))
            self.cursor.execute(self.sqlStatements.drop('hours'))
            self.conn.commit()


db = Db()
