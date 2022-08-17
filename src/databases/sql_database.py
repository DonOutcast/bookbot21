import sqlite3 as sq
import time

from src.create_bot import bot


class DatabaseBot:
    def __init__(self, name):
        self.name = name
        self.base = sq.connect(f"{self.name}")
        self.cur = self.base.cursor()

    def sql_create_users(self):
        if self.base:
            print("Data base connected OK!")
            self.cur.execute(
                """CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY,            
                                                    login VARCHAR(20),
                                                    role VARCHAR(20),
                                                    campus Varchar(20)
                                                    )"""
            )
            self.base.commit()

    def sql_create_booking(self):
        if self.base:
            print("Data base connected OK!")
            self.cur.execute(
                """CREATE TABLE IF NOT EXISTS booking ( id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                        date DATE,
                                                        start_time VARCHAR(10) ,
                                                        end_time VARCHAR(10),
                                                        status INTEGER,
                                                        description VARCHAR(50),
                                                        user_id INTEGER,
                                                        object_id INTEGER
                                                        )"""
            )
            self.base.commit()

    def sql_create_objects(self):
        if self.base:
            print("Data base connected OK!")
            self.cur.execute(
                """CREATE TABLE IF NOT EXISTS objects ( id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                        name VARCHAR(30),
                                                        type VARCHAR(20),
                                                        description VARCHAR(50),
                                                        campus VARCHAR(20),
                                                        floor INTEGER,
                                                        number_of_the_room INTEGER,
                                                        image TEXT
                                                        )"""
            )
            self.base.commit()

    async def sql_add_users(self, state: list) -> int:
        async with state.proxy() as data:
            self.cur.execute('INSERT INTO users VALUES(?, ?, ?, ?);', (tuple(data.values())))
            self.base.commit()

    async def sql_output_all_users(self):
        return self.cur.execute("SELECT * FROM users").fetchall()

    async def sql_add_objects(self, state):
        async with state.proxy() as data:
            print(tuple(data.values()))
            self.cur.execute('''INSERT INTO objects (name, type, description, campus, floor, number_of_the_room, image)
                                VALUES(?, ?, ?, ?, ?, ?, ?);''', (tuple(data.values())))
            self.base.commit()

    # async def sql_output(self, message):
    #     for ret in self.cur.execute("SELECT * FROM objects").fetchall():
    #         await bot.send_photo(message.from_user.id, ret[7],
    #                              f'{ret[0]}\n {ret[1]}\n {ret[2]}\n {ret[3]}\n {ret[4]}\n {ret[5]}\n {ret[6]}')

    async def sql_my_booking(self, user_id):
        ret = self.cur.execute('''  SELECT booking.description, objects.type, objects.name, objects.campus, objects.floor, objects.number_of_the_room, booking.date, booking.start_time, booking.end_time
                                    FROM objects
                                    JOIN booking
                                    On objects.id=booking.object_id
                                    WHERE booking.user_id=?''', (user_id,)
                               ).fetchall()
        return ret

    async def sql_check_booking(self, date):
        ret = self.cur.execute('''  SELECT booking.start_time, booking.end_time
                                    FROM booking
                                    WHERE booking.date=? AND status=1''', (date,)
                               ).fetchall()
        return ret

    async def sql_cancel_booking(self, booking_id):
        self.cur.execute(''' UPDATE booking 
                            SET status=?
                            WHERE id=?''', (0, booking_id))
        self.base.commit()

    async def sql_check_rule(self, user_id):
        ret = self.cur.execute('''SELECT role
                                            FROM users
                                            WHERE id=?''', (user_id, )
                               ).fetchone()
        return ret

    async def sql_booking(self, state):
        async with state.proxy() as data:
            data = tuple(data.values())
            print(data)
            ret = self.cur.execute('''  SELECT objects.id
                                        FROM objects
                                        JOIN users
                                        On objects.campus=users.campus
                                        WHERE objects.type=? and objects.name=?
                                        LIMIT 1''', (data[2], data[3])
                                   ).fetchone()
            if ret is not None:
                self.cur.execute('INSERT INTO booking ( start_time, end_time ,status, description, user_id, object_id, date ) VALUES(?, ?, ?, ?, ?, ?, ?);', (data[-2], data[-1], 1, data[1], data[0], ret[0], data[-3]))
                self.base.commit()
            else:
                print("Ошибка бронирования")

    async def check_registration(self, user_id) -> bool:
        return self.cur.execute("SELECT id FROM users WHERE id=?", (user_id,)).fetchone() is not None

