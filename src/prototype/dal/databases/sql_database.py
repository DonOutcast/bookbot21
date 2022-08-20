import sqlite3 as sq


from prototype.basicui.keyboards.inline_kb import create_button
from prototype.kernel.create_bot import bot



class DatabaseBot:
    def __init__(self, name):
        self.name = name
        self.base = sq.connect(f"{self.name}")
        self.cur = self.base.cursor()

    def sql_create_users(self):
        if self.base:
            print("Data base: table users connected OK!")
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
            print("Data base: table booking connected OK!")
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
            print("Data base: table objects connected OK!")
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

    async def sql_add_users(self, state):
        async with state.proxy() as data:
            self.cur.execute('INSERT INTO users VALUES(?, ?, ?, ?);', (tuple(data.values())))
            self.base.commit()

    async def sql_output_all_users(self):
        return self.cur.execute("SELECT * FROM users").fetchall()

    async def sql_add_objects(self, state):
        async with state.proxy() as data:
            self.cur.execute('''INSERT INTO objects (name, type, description, campus, floor, number_of_the_room, image)
                                VALUES(?, ?, ?, ?, ?, ?, ?);''', (tuple(data.values())))
            self.base.commit()

    async def sql_my_booking(self, user_id, full=True):
        lst = self.cur.execute('''  SELECT  booking.description, objects.type,
                                            objects.name, objects.campus,
                                            objects.floor, objects.number_of_the_room,
                                            booking.date, booking.start_time,
                                            booking.end_time, booking.description,
                                            objects.image, booking.id
                                    FROM objects
                                    JOIN booking
                                    On objects.id=booking.object_id
                                    WHERE booking.user_id=? AND booking.status=(?)''', (user_id, 1,)
                               ).fetchall()
        if len(lst) == 0:
            await bot.send_message(user_id, "У вас еще нету броней ")

        if full:
            for ret in iter(lst):
                await bot.send_photo(user_id, ret[10], f'Мероприятие: {ret[9]}\n'
                                                       f'Название объекта: {ret[2]}\n'
                                                       f'Тип объекта: {ret[1]}\n'
                                                       f'Кампус: {ret[3]}\n'
                                                       f'Этаж: {ret[4]}\n'
                                                       f'Местоположение: {ret[5]}\n'
                                                       f'Время бронирования: {ret[6]} {ret[7]}-{ret[8]}\n',
                                     reply_markup=create_button(ret[11]))
        else:
            ret = lst[-1]
            await bot.send_photo(user_id, ret[10], f'Мероприятие: {ret[9]}\n'
                                                   f'Название объекта: {ret[2]}\n'
                                                   f'Тип объекта: {ret[1]}\n'
                                                   f'Кампус: {ret[3]}\n'
                                                   f'Этаж: {ret[4]}\n'
                                                   f'Местоположение: {ret[5]}\n'
                                                   f'Дата бронирования: {ret[6]}\n'
                                                   f'Время бронирования: {ret[7]}-{ret[8]}\n',
                                 reply_markup=create_button(ret[11]))

    async def sql_check_booking(self, date, object_id):
        ret = self.cur.execute('''  SELECT booking.start_time, booking.end_time
                                    FROM booking
                                    WHERE booking.date=? AND status=1 AND object_id=?''', (date, object_id,)
                               ).fetchall()
        return ret

    async def sql_object_type(self, user_id):
        ret = self.cur.execute('''  SELECT DISTINCT type
                                    FROM objects
                                    JOIN users
                                    ON objects.campus = users.campus
                                    WHERE users.id=?
                                    ''', (user_id, )
                               ).fetchall()
        return ret

    async def sql_list_object(self, type_name):
        ret = self.cur.execute('''  SELECT DISTINCT id, name
                                    FROM objects
                                    WHERE type=?
                                    ''', (type_name, )
                               ).fetchall()
        return ret

    async def sql_cancel_booking(self, booking_id):
        self.cur.execute('''UPDATE booking 
                            SET status=?
                            WHERE id=?''', (0, int(booking_id)))
        self.base.commit()

    async def sql_check_rule(self, user_id):
        ret = self.cur.execute('''  SELECT role
                                    FROM users
                                    WHERE id=?''', (user_id, )
                               ).fetchone()
        return ret

    async def sql_get_id(self, state):
        async with state.proxy() as data:
            data = tuple(data.values())
            ret = self.cur.execute('''  SELECT objects.id
                                        FROM objects
                                        JOIN users
                                        On objects.campus=users.campus
                                        WHERE objects.type=? and objects.name=?
                                        LIMIT 1''', (data[2], data[3])
                                   ).fetchone()
        return ret

    async def sql_booking(self, data) -> bool:
        ret = self.cur.execute('''  SELECT objects.id
                                    FROM objects
                                    JOIN users
                                    On objects.campus=users.campus
                                    WHERE objects.type=? and objects.name=?
                                    LIMIT 1''', (data[2], data[3])
                               ).fetchone()
        if ret is not None:
            self.cur.execute('INSERT INTO booking'
                             '(start_time, end_time ,status, description, user_id, object_id, date)'
                             'VALUES(?, ?, ?, ?, ?, ?, ?);',
                             (data[-2], data[-1], 1, data[1], data[0], data[4], data[5]))
            self.base.commit()
            return True
        return False

    async def check_registration(self, user_id) -> bool:
        return self.cur.execute("SELECT id FROM users WHERE id=?", (user_id,)).fetchone() is not None

    async def sql_get_login(self, user_id) -> list:
        return self.cur.execute("SELECT login FROM users WHERE id=(?)", (user_id, )).fetchone()

    async def sql_user_info(self, user_id):
        return self.cur.execute("SELECT login, role, campus FROM users WHERE id=(?)", (user_id, )).fetchall()
