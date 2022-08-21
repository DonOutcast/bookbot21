from aiogram import types
from prototype.kernel.create_bot import bot
from aiogram.types import ContentType
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from prototype.dal.databases.init_database import user_db
from aiogram.dispatcher.filters.state import State, StatesGroup
from prototype.basicui.keyboards.system_kb import back_menu_keyboard, keyboards_menu
from prototype.basicui.my_calendar.inline_calendar import get_date, filter_list_date
from prototype.basicui.my_calendar.inline_time_list import get_time, filter_list_time
from prototype.basicui.keyboards.inline_generation import filter_list, inline_type_list, inline_object_list


class Student(StatesGroup):
    user_id = State()
    description = State()
    type_of_object = State()
    name_of_object = State()
    object_id = State()
    user_date = State()


class Booking:

    def __init__(self, dp):
        self.dp = dp

    @staticmethod
    async def where_is_webb(message: types.Message, state: FSMContext):
        await message.delete()
        check_web = message.web_app_data.data
        rule = await user_db.sql_check_rule(message.from_user.id)
        if rule is not None:
            if rule[0] == 'intensivist' and check_web != 'Переговорные':
                await message.answer(
                    "Переговорные могут бронировать абсолютно все зарегестрированные пользователи, обратитесь к Адм для более поддробной информации")
                await bot.send_sticker(message.from_user.id,
                                       sticker="CAACAgIAAxkBAAENoSNjAhELud-r6x09cJy3tDtLOHpsTQACFgkAAmMr4gl0V-nVbS6gKSkE")
            elif rule[0] != 'adm' and check_web == 'Кухня':
                await bot.send_sticker(message.from_user.id,
                                       sticker="CAACAgIAAxkBAAENoSFjAhCS3nF4bBzGowf4QOW-NlBnDwACBwkAAmMr4gm4fe-IbYPq_ikE")
            elif rule[0] != 'adm' and check_web == 'Кластер':
                await bot.send_sticker(message.from_user.id,
                                       sticker="CAACAgIAAxkBAAENoR9jAhCFgEFfU179_uRqbvAxJ-kGMAACFAkAAmMr4gkYTOPUAyUdRSkE")
            else:
                async with state.proxy() as data:
                    data['type_of_object'] = check_web
                await Booking.cmd_booking(message=message, state=state)
        else:
            await message.answer(
                "Для того чтобы забронировать чтото из этого списка, пройдите регестрацию")
            await bot.send_sticker(message.from_user.id,
                                   sticker="CAACAgEAAxkBAAENobdjAkWbhOAfHoHPXsxLBB90mrOGFQACMQIAAsOjKEdLBVdiYsQQXykE")
    @staticmethod
    async def cmd_booking(message: types.Message, state: FSMContext):
        rule = await user_db.sql_check_rule(message.from_user.id)
        if rule is not None:
            await Student.first()
            async with state.proxy() as data:
                data['user_id'] = message.from_user.id
            await Student.next()
            await message.answer("Введите описание мероприятия", reply_markup=back_menu_keyboard)
            await bot.send_sticker(message.from_user.id,
                                   sticker="CAACAgEAAxkBAAENoVljAh8xTOx1Nmxyk4ruq8V7cITCYQAC7AcAAuN4BAAB6DEEbU_xFOwpBA")
        else:
            await message.answer("Зарегестрируйся для бронирования объектов")

    @staticmethod
    async def log_user_answer_1(message: types.Message, state: FSMContext):
        if message.content_type != 'text':
            await message.answer("Сюда нужно ввести только текст!!!!")
            await bot.send_sticker(message.from_user.id,
                                   sticker="CAACAgIAAxkBAAENm11i_0WUEosLLgLt0thPR5z5pRr3ggACoQcAAmMr4gm9FrBamSBazCkE")
            await message.delete()
            await Student.description.set()
            await message.answer("Введите описание мероприятия", reply_markup=back_menu_keyboard)
        else:
            async with state.proxy() as data:
                data['description'] = message.text

                new_keyboard, ret = await inline_type_list(user_db, message.from_user.id)
                if ret:
                    if 'type_of_object' in data.keys():
                        await message.answer('Выберите объект:',
                                             reply_markup=await inline_object_list(user_db, data["type_of_object"]))
                        await Student.name_of_object.set()
                    else:
                        await message.answer("Выберите тип объекта", reply_markup=new_keyboard)
                        await Student.next()
                else:
                    await message.answer("Не найдено доступных для бронирования объектов", reply_markup=keyboards_menu)




    @staticmethod
    async def check_choice_type(message: types.Message):
        await message.delete()
        await message.answer("Выберите нужный вам тип по кнопкам!!!!!", reply_markup=back_menu_keyboard)

    @staticmethod
    async def log_user_answer_2(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
        await callback.answer()
        await callback.message.delete()
        await callback.message.answer('Выберите объект:',
                               reply_markup=await inline_object_list(user_db, callback_data["id"]))
        async with state.proxy() as data:
            data['type_of_object'] = callback_data['id']
        await Student.next()
        await callback.message.answer("Выберите название объекта")

    @staticmethod
    async def check_choice_name(message: types.Message):
        await message.delete()
        await message.answer("Выберите нужный вам тип по кнопкам!!!!!", reply_markup=back_menu_keyboard)

    @staticmethod
    async def log_user_answer_3(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
        await callback.message.delete()
        async with state.proxy() as data:
            data['name_of_object'] = callback_data["id"]
        await Student.next()
        object_id = await user_db.sql_get_id(state)
        if object_id:
            async with state.proxy() as data:
                data['object_id'] = object_id[0]
            await Student.next()
            await callback.message.answer("Выберите дату", reply_markup=await get_date())
        else:
            await state.finish()
            await callback.message.answer("Данный объект вам не доступен", reply_markup=keyboards_menu)

    @staticmethod
    async def enter_test_1(callback_query: types.CallbackQuery, callback_data: dict):
        await callback_query.answer()
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=callback_query.message.text,
            reply_markup=await get_date(callback_data['date']))

    @staticmethod
    async def check_choice_date(message: types.Message):
        await message.delete()
        await message.answer("Выберите нужную вам дату(время) из календаря", reply_markup=back_menu_keyboard)

    @staticmethod
    async def enter_test_2(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
        await callback_query.answer()
        await callback_query.message.delete()
        date = callback_data.get("date")
        async with state.proxy() as data:
            object_id = data['object_id']
        await callback_query.message.answer(text=f'Дата: {date}\nВыберите время начала',
                                            reply_markup=await get_time(date=date,
                                                                        object_id=object_id))

    @staticmethod
    async def enter_test_3(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
        await callback_query.answer()
        async with state.proxy() as data:
            object_id = data['object_id']
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=callback_query.message.text.replace('Выберите время начала', 'Выберите время конца'),
            reply_markup=await get_time(date=callback_data['date'],
                                        start_time=callback_data['first_time'],
                                        object_id=object_id))

    @staticmethod
    async def enter_test_4(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
        await callback_query.answer()
        await callback_query.message.delete()
        date = callback_data['date']
        start_time = callback_data['first_time']
        end_time = callback_data['last_time']
        async with state.proxy() as data:
            data = data['user_id'], data['description'], data['type_of_object'], data['name_of_object'], data['object_id']
        data = (*data, date, start_time, end_time)
        query = await user_db.sql_booking(data)
        await state.finish()
        if query:
            login = await user_db.sql_get_login(callback_query.from_user.id)
            await callback_query.message.answer(f"Вы {login[0]} успешно забранировали!")
            await user_db.sql_my_booking(callback_query.from_user.id, False)
        else:
            await callback_query.message.answer(text="Ощибка бронирования")

    @staticmethod
    async def remove_calendar(callback_query: types.CallbackQuery, state: FSMContext):
        await state.finish()
        await callback_query.message.delete()

    def register_handlers_student(self):
        # self.dp.register_message_handler(self.chek_web_apps)
        self.dp.register_message_handler(self.where_is_webb, content_types='web_app_data')
        self.dp.register_message_handler(self.cmd_booking, lambda message: 'Бронирование ✅' in message.text, state=None)

        self.dp.register_message_handler(self.log_user_answer_1, state=Student.description,
                                         content_types=[ContentType.ANY])
        self.dp.register_message_handler(self.check_choice_type, state=Student.type_of_object,
                                         content_types=[ContentType.ANY])
        self.dp.register_callback_query_handler(self.log_user_answer_2,
                                                filter_list.filter(action='get_type_list'),
                                                state=Student.type_of_object)
        self.dp.register_message_handler(self.check_choice_name, state=Student.name_of_object,
                                         content_types=[ContentType.ANY])
        self.dp.register_callback_query_handler(self.log_user_answer_3,
                                                filter_list.filter(action='get_object_list'),
                                                state=Student.name_of_object)
        self.dp.register_callback_query_handler(self.enter_test_1, filter_list_date.filter(type='refresh'),
                                                state=Student.user_date)
        self.dp.register_callback_query_handler(self.remove_calendar, Text(equals="cancel_calendar"),
                                                state=Student.user_date)
        self.dp.register_message_handler(self.check_choice_date, state=Student.user_date)
        self.dp.register_callback_query_handler(self.enter_test_2, filter_list_date.filter(type='get_date'),
                                                state=Student.user_date)
        self.dp.register_callback_query_handler(self.enter_test_3, filter_list_time.filter(type='first'),
                                                state=Student.user_date)
        self.dp.register_callback_query_handler(self.enter_test_4, filter_list_time.filter(type='last'),
                                                state=Student.user_date)
