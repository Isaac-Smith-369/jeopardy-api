import sqlite3

class DevDB:

    def __init__(self, file: str = ""):
        self.file = file

    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        return self.conn, self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.close()

