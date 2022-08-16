import sqlite3 as sq


class DatabaseBot:

    def __init__(self, name):
        self.name = name
        self.base = sq.connect(f"{self.name}")
        self.cur = self.base.cursor()

    def sql_create_users(self):
        if self.base:
            print("Data base connected OK!")
            self.cur.execute("""CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, login VARCHAR(20), role VARCHAR(20), campus Varchar(20))""")
            self.base.commit()

    def sql_create_booking(self):
        if self.base:
            print("Data base connected OK!")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS booking(start_time DATE, end_time DATE, status INTEGER, user_id INTEGER, object_id INTEGER)""")
        self.base.commit()

    def sql_create_objects(self):
        if self.base:
            print("Data base connected OK!")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS objects(id INTEGER PRIMARY KEY, name VARCHAR(30), type VARCHAR(20), description VARCHAR(50), campus VARCHAR(20), floor INTEGER, number_of_the_room INTEGER, image TEXT)""")
        self.base.commit()

    def add_user(self, user_id, login, role, campus):
        self.cur.execute("""INSERT INTO user VALUES(?, ?, ?, ?);, ()""")
