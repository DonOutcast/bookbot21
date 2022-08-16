import sqlite3 as sq
from bookbot21.src.create_bot import bot


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
        self.cur.execute("""CREATE TABLE IF NOT EXISTS objects(id INTEGER PRIMARY KEY , name VARCHAR(30), type VARCHAR(20), description VARCHAR(50), campus VARCHAR(20), floor INTEGER, number_of_the_room INTEGER, image TEXT)""")
        self.base.commit()

    async def sql_add_objects(self, state):
        async with state.proxy() as data:
            print(data)
            self.cur.execute('INSERT INTO objects VALUES(?, ?, ?, ?, ?, ?, ?, ?);', (tuple(data.values())))
            self.base.commit()

    async def sql_output(self, message):
        for ret in self.cur.execute("SELECT * FROM objects").fetchall():
            await bot.send_photo(message.from_user.id, ret[7], f'{ret[0]}\n {ret[1]}\n {ret[2]}\n {ret[3]}\n {ret[4]}\n {ret[5]}\n {ret[6]}')
