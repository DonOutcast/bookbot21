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
    async def cmd_booking(message: types.Message, state: FSMContext):
        rule = await user_db.sql_check_rule(message.from_user.id)
        if rule is not None:
            await Student.first()
            async with state.proxy() as data:
                data['user_id'] = message.from_user.id
            await Student.next()
            await message.answer("Введите описание мероприятия", reply_markup=back_menu_keyboard)
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
            await Student.next()
            new_keyboard, ret = await inline_type_list(user_db, message.from_user.id)
            if ret:
                await message.answer("Выберите тип объекта", reply_markup=new_keyboard)
            else:
                await message.answer("Не найдено доступных для бронирования объектов", reply_markup=keyboards_menu)

    @staticmethod
    async def check_choice_type(message: types.Message):
        await message.delete()
        await message.answer("Выберите нужный вам тип по кнопкам!!!!!")

    @staticmethod
    async def log_user_answer_2(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
        await callback.answer()
        await callback.message.delete()
        await callback.message.answer('Выберите объект:',
                                      reply_markup=await inline_object_list(user_db, callback_data['id']))
        async with state.proxy() as data:
            data['type_of_object'] = callback_data['id']
        await Student.next()
        await callback.message.answer("Выберите название объекта")

    @staticmethod
    async def check_choice_name(message: types.Message):
        await message.delete()
        await message.answer("Выберите нужный вам тип по кнопкам!!!!!")

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
        await message.answer("Выберите нужную вам дату(время) из календаря")

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
            data = tuple(data.values())
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
