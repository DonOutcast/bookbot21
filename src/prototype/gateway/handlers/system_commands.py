import os
from prototype.kernel.create_bot import bot
from aiogram.types import ContentType
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from prototype.dal.databases.init_database import user_db
from prototype.basicui.keyboards.inline_kb import filter_drop_booking
from prototype.basicui.keyboards.inline_kb import city_markup, users_markup
from aiogram.dispatcher.filters.state import State, StatesGroup
from prototype.basicui.keyboards.system_kb import keyboards_menu, back_menu_keyboard
from prototype.kernel.config import ADM_PASSWORD, STUDENT_PASSWORD, INTENSIVIST_PASSWORD

count = 0


class Registration(StatesGroup):
    user_id = State()
    user_name = State()
    user_role = State()
    check_password = State()
    campus_name = State()


def output_warning(name_of_button) -> str:
    if name_of_button == 'adm':
        result = "Админа 🦁"
    elif name_of_button == 'student':
        result = "Студента 👨‍💻"
    else:
        result = "Интенсивиста 🥷"
    return result


class BaseCommands:
    def __init__(self, dp):
        self.dp = dp

    @staticmethod
    async def cmd_reg(message: types.Message, state: FSMContext):
        check = await user_db.check_registration(message.from_user.id)
        if not check:
            await Registration.first()
            async with state.proxy() as data:
                data['user_id'] = message.from_user.id
            await Registration.next()
            await bot.send_message(message.from_user.id, "Введите логин для авторизации!",
                                   reply_markup=back_menu_keyboard)
        else:
            await message.answer("Вы уже зарегистрированы!")

    @staticmethod
    async def cmd_cancel_registration(message: types.Message, state: FSMContext):
        await message.delete()
        try:
            await bot.delete_message(message.from_user.id, message_id=message.message_id - 1)
        except:
            pass
        current_state = await state.get_state()
        if current_state is None:
            await message.answer('Вы вернулись в главное меню', reply_markup=keyboards_menu)
            await bot.send_sticker(message.from_user.id,
                                   sticker="CAACAgIAAxkBAAENm1Bi_0Q9YClvUdjgvDLx0S5V3Z3UUgAClgcAAmMr4glEcXCvl0uDLSkE")
            return
        await state.finish()
        await message.answer('Вы вернулись в главное меню', reply_markup=keyboards_menu)
        await bot.send_sticker(message.from_user.id,
                               sticker="CAACAgIAAxkBAAENm1Bi_0Q9YClvUdjgvDLx0S5V3Z3UUgAClgcAAmMr4glEcXCvl0uDLSkE")

    @staticmethod
    async def user_answer_1(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['user_name'] = message.text
            await Registration.next()
            await message.answer("Выберите вашу роль!", reply_markup=users_markup)

    @staticmethod
    async def check_choice_login(message: types.Message):
        await message.delete()
        await message.answer("Введите имя нормальным текстом 📝!")
        await bot.send_sticker(message.from_user.id,
                               sticker="CAACAgIAAxkBAAENm2di_0hRuQh_CEYY4vCtbwzpbMw_BQACcQgAAoSUQUlvaAkaprvOcykE")

    @staticmethod
    async def user_answer_2(callback: types.CallbackQuery, state: FSMContext):
        name = callback.data.split("_")[1]
        async with state.proxy() as data:
            data['user_role'] = name
        await Registration.next()
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=callback.message.text,
            reply_markup=None)
        name = output_warning(name)
        await callback.message.answer("Ведите свой уникальный токен: ")
        await callback.answer(f"Для подтверждения роли {name}, вам необходимо будет ввести токен", show_alert=True)

    @staticmethod
    async def check_choice_role(message: types.Message):
        await message.delete()
        await message.answer("Я прошу тебя лишь об одном нажми на кнопку ")
        await bot.send_sticker(message.from_user.id,
                               sticker="CAACAgIAAxkBAAENm1hi_0U1efcDilnmrARFOO3lRh36JAACmQcAAmMr4gmx63jV6i42GSkE")

    @staticmethod
    async def check_password(message: types.Message, state: FSMContext):
        global count
        if message.content_type != 'text':
            await message.delete()
            await message.answer("Введите свой токен просто токен, простым текстом 📝")
            await bot.send_sticker(message.from_user.id,
                                   sticker="CAACAgIAAxkBAAENm2di_0hRuQh_CEYY4vCtbwzpbMw_BQACcQgAAoSUQUlvaAkaprvOcykE")
            await Registration.check_password.set()
            await message.answer("Ведите свой уникальный токен: 📝")
        else:
            count += 1
            pasword = message.text
            data = await state.get_data()
            if pasword == ADM_PASSWORD and data['user_role'] == 'adm':
                await Registration.next()
                count = 0
                await message.answer("Из какого вы кампуса", reply_markup=city_markup)
            elif pasword == STUDENT_PASSWORD and data['user_role'] == 'student':
                await Registration.next()
                count = 0
                await message.answer("Из какого вы кампуса", reply_markup=city_markup)
            elif pasword == INTENSIVIST_PASSWORD and data['user_role'] == 'intensivist':
                await Registration.next()
                count = 0
                await message.answer("Из какого вы кампуса", reply_markup=city_markup)
            else:
                await message.answer("Неверный токен!!!")
                await message.answer("Попробуйте еще раз")
                await Registration.check_password.set()
                if count == 3:
                    await message.answer("Попробуйте сначала")
                    await state.finish()

    @staticmethod
    async def user_answer_3(callback: types.CallbackQuery, state: FSMContext):
        city = callback.data.split('_')[1]
        async with state.proxy() as data:
            data['campus_name'] = city
        await user_db.sql_add_users(state)
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=callback.message.text,
            reply_markup=None)
        await callback.message.answer("Вы успешно зарегестрировались", reply_markup=keyboards_menu)
        await bot.send_sticker(callback.message.chat.id,
                               sticker="CAACAgIAAxkBAAENmyxi_0A_bLGhxU5z4Px-EI-3h1kNdgACnQcAAkb7rAT8KJ0CtQxURikE")
        await state.finish()

    @staticmethod
    async def check_choice_city(message: types.Message):
        await message.delete()
        await message.answer("Я прошу тебя лишь об одном нажми на кнопку")
        await bot.send_sticker(message.from_user.id,
                               sticker="CAACAgIAAxkBAAENm1hi_0U1efcDilnmrARFOO3lRh36JAACmQcAAmMr4gmx63jV6i42GSkE")

    @staticmethod
    async def cmd_start(message: types.Message):

        path = os.path.abspath('photo/title.jpeg')
        with open(path, 'rb') as photo:
            await bot.send_photo(message.from_user.id,
                                 photo=photo)
        await bot.send_message(message.from_user.id, "Добро пожаловать!\nЗдесь вы можете оформить бронь",
                               reply_markup=keyboards_menu)
        await message.delete()

    @staticmethod
    async def cmd_show(message: types.Message):
        read = await user_db.sql_output_all_users()
        await message.answer(read)

    @staticmethod
    async def cmd_my(message: types.Message):
        await user_db.sql_my_booking(message.from_user.id)

    @staticmethod
    async def delete_booking(callback: types.CallbackQuery, callback_data: dict):
        await user_db.sql_cancel_booking(callback_data['booking_id'])
        await callback.answer("Бронь успешно отменена ", show_alert=True)
        await callback.message.delete()

    @staticmethod
    async def cmd_my_self(message: types.Message):
        check = await user_db.check_registration(message.from_user.id)
        if not check:
            await message.answer("Пройдите регистрацию для получения информации")
            await bot.send_sticker(message.from_user.id,
                                   sticker="CAACAgIAAxkBAAENnVli__hWmaC7OjLLpkNXNxRxTOdcnwACnwcAAmMr4gnSznx_gKZbQSkE")
        else:
            ret = await user_db.sql_user_info(message.from_user.id)
            login, role, campus = ret[0]
            await message.answer(f"\ntg: @{message.from_user.username}"
                                 f"\nID: {message.from_user.id}"
                                 f"\nЛогин: {login}"
                                 f"\nРоль: {role}"
                                 f"\nКампус: {campus}")

    @staticmethod
    async def cmd_information(message: types.Message):
        await message.answer("\nЭто бот для бронирования различных объектов в кампусах школы 21."
                             "\nВ зависимости от вашей роли и вашего кампуса вам доступны различные объекты"
                             "\nВ настоящий момент есть возможность забронировать")
        await message.answer_photo(
            "https://cdnstatic.rg.ru/uploads/images/gallery/cf7d1196/6_394ce4c8.jpg",
            "ПЕРЕГОВОРКИ и КОНФЕРЕНЦ-ЗАЛЫ"
        )
        await message.answer_photo(
            "https://zvetnoe.ru/upload/images/blog/063_Nastolnye_igry/1.jpg",
            "НАСТОЛЬНЫЕ ИГРЫ"
        )
        await message.answer_photo(
            "https://sadovod-torg.ru/assets/images/katalog/sport-i-otdyix/sportinventar/imgSlider1_1.jpg",
            "СПОРТИВНЫЙ ИНВЕНТАРЬ"
        )

    @staticmethod
    async def where_is_webb(message: types.Message):
        await message.delete()
        check_web = message.web_app_data.data
        if check_web == '1':
            await message.answer(
                "Переговорные могут бронировать абсолютно все зарегестрированные пользователи.\nДля брони перейдите в раздель бронирования")
            await bot.send_sticker(message.from_user.id,
                                   sticker="CAACAgIAAxkBAAENndVjAAEd9BY2V5NQn3nZISwI4kaizMwAAgQJAAJjK-IJ5dZK0lV5eW8pBA")
        elif check_web == '2':
            await message.answer(
                "Настольные игру могут бронировавть только студенты и сотрудники адм, так что дружок учи указатели.\nДля брони перейдите в раздель бронирования")
            await bot.send_sticker(message.from_user.id,
                                   sticker="CAACAgIAAxkBAAENndNjAAEd0U3Ew_DF5llFH3LC-fljfk4AAhYJAAJjK-IJdFfp1W0uoCkpBA")
        elif check_web == '3':
            await message.answer(
                "Книжки могут читать только студенты и сотрудники адм.\nДля брони перейдите в раздель бронирования")
            await bot.send_sticker(message.from_user.id,
                                   sticker="CAACAgIAAxkBAAENndFjAAEdp-xGZdv6bzIH9rEMGPOECbUAAggJAAJjK-IJfU4QLscFhMEpBA")
        elif check_web == '4':
            await message.answer(
                "Спортом могут заниматься  только студенты и сотрудники адм.\nДля брони перейдите в раздель бронирования")
            await bot.send_sticker(message.from_user.id,
                                   sticker="CAACAgIAAxkBAAENnc9jAAEc9QgKnCmr4WDklv_y2B81CBwAAooGAALSWogBvRxYp7K-XakpBA")

    def register_handlers_system(self):
        self.dp.register_message_handler(self.cmd_start, commands=["start"])
        self.dp.register_message_handler(self.cmd_cancel_registration, Text(equals="Вернуться в главное меню 📜"),
                                         state="*")
        self.dp.register_message_handler(self.cmd_reg, lambda message: "Регистрация 🔐" in message.text, state=None)
        self.dp.register_message_handler(self.user_answer_1, state=Registration.user_name)
        self.dp.register_message_handler(self.check_choice_login, state=Registration.user_name,
                                         content_types=[ContentType.ANY])
        self.dp.register_callback_query_handler(self.user_answer_2, Text(startswith="user_"),
                                                state=Registration.user_role)
        self.dp.register_message_handler(self.check_choice_role, state=Registration.user_role,
                                         content_types=[ContentType.ANY])
        self.dp.register_message_handler(self.check_password, state=Registration.check_password,
                                         content_types=[ContentType.ANY])
        self.dp.register_callback_query_handler(self.user_answer_3, Text(startswith="city_"),
                                                state=Registration.campus_name)
        self.dp.register_message_handler(self.check_choice_city, state=Registration.campus_name,
                                         content_types=[ContentType.ANY])
        self.dp.register_message_handler(self.cmd_show, commands=["show"], content_types=[ContentType.ANY])
        self.dp.register_message_handler(self.cmd_my, lambda message: "Мои брони 📝" in message.text)
        self.dp.register_message_handler(self.cmd_my_self, lambda message: "О себе 🆘" in message.text)
        self.dp.register_message_handler(self.cmd_information, lambda message: "Информация ⚠" in message.text)
        self.dp.register_callback_query_handler(self.delete_booking, filter_drop_booking.filter(action="bye_booking"))
        self.dp.register_message_handler(self.where_is_webb, content_types='web_app_data')
