import sqlite3 as sq


class DatabaseBot:

    def __init__(self, name):
        self.name = name
        self.base = sq.connect(f"{self.name}")
        self.cur = self.base.cursor()

    def sql_start(self):
        if self.base:
            print("Data base connected OK!")
        self.cur.execute("""CREATE TABLE IS NOT EXISTS users(id INTEGER PRIMARY KEY, login VARCHAR(20), role VARCHAR(20),
                          campus Varchar(20);""")

        self.cur.commit()
