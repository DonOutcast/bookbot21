import time
from datetime import date
from aiogram import types, Dispatcher
from src.create_bot import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from src.databases import sql_database
from src.config import ADM_PASSWORD, STUDENT_PASSWORD, INTENSIVIST_PASSWORD
from src.handlers.admin import user_db


class Student(StatesGroup):
    user_id = State()
    description = State()
    # check_rule = State()
    type_of_object = State()
    name_of_object = State()
    user_date = State()
    start_time = State()
    end_time = State()



# @dp.message_handlers(commands=['/booking'], state=None)
async def cmd_booking(message: types.Message, state: FSMContext):
    await Student.first()
    async with state.proxy() as data:
        data['user_id'] = message.from_user.id
    await Student.next()
    await message.answer("Введите описание мероприятия")


# @dp.message_handlers(state=Student.description)
async def log_user_answer_1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await Student.next()
    await message.answer("Выберите тип объекта")
    rule = await user_db.sql_check_rule(message.from_user.id)
    if "".join(rule) == 'adm':
        await message.answer("Game")


# @dp.message_handlers(state=Student.type_of_object)
async def log_user_answer_2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['type_of_object'] = message.text
    await Student.next()
    await message.answer("Выберите название объекта")

# # @dp.message_handler(state=Student.check_rule)
# async def check_rule(message: types.Message, state: FSMContext):
#
#     rule = await user_db.sql_check_rule(message.from_user.id)
#     if rule == 'adm' and


# @dp.message_handlers(state=Student.name_of_object)
async def log_user_answer_3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_of_object'] = message.text
    await Student.next()
    await message.answer("Выберите дату")


# @dp.message_handler(state=Student.user_date)
async def log_user_answer_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_data'] = message.text
    await Student.next()
    await message.answer("Выберите время начала бронирования")

# @dp.message_handlers(state=Student.start_time)
async def log_user_answer_4(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['start_time'] = message.text
    await Student.next()
    await message.answer("Выберите дату , время конца бронирования")


# @dp.message_handlers(state=Student.start_time)
async def log_user_answer_5(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['end_time'] = message.text
    query = await user_db.sql_booking(state, message)
    await state.finish()
    if query:
        login = await user_db.sql_get_login(message.from_user.id)
        await message.answer(f"Вы {login[0]} успешно забранировали!")
        await user_db.sql_my_booking(message, False)
    else:
        await bot.send_message(message.from_user.id, text="Ощибка бронирования")


def register_handlers_student(dp: Dispatcher):
    dp.register_message_handler(cmd_booking, lambda message: 'Бронирование ✅' in message.text, state=None)
    dp.register_message_handler(log_user_answer_1, state=Student.description)
    dp.register_message_handler(log_user_answer_2, state=Student.type_of_object)
    dp.register_message_handler(log_user_answer_date, state=Student.user_date)
    dp.register_message_handler(log_user_answer_3, state=Student.name_of_object)
    dp.register_message_handler(log_user_answer_4, state=Student.start_time)
    dp.register_message_handler(log_user_answer_5, state=Student.end_time)

