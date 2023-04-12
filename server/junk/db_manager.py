import sqlite3


class DBManager:
    def __init__(self, name):
        self.name = name
        self.db_name = f'{name}.db'
        self.connection = sqlite3.connect(self.db_name)

    def get_cursor(self):
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()

    @staticmethod
    def setup(name):
        connection = sqlite3.connect(f'{name}.db')
        cursor = connection.cursor()
        try:
            cursor.execute("CREATE TABLE nodes (id TEXT PRIMARY KEY, ip TEXT)")
            cursor.execute("CREATE TABLE data_addresses (id TEXT PRIMARY KEY, name TEXT, address TEXT)")
            cursor.execute(
                "CREATE TABLE my_chunks (part_id TEXT, cid TEXT, rep1_address TEXT, rep2_address TEXT, rep3_address TEXT)")
        except sqlite3.OperationalError:
            pass

