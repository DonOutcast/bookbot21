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
    type_of_object = State()
    name_of_object = State()
    start_time = State()
    end_time = State()


# @dp.message_hadler(commands=['/booking'], state=None)
async def cmd_booking(message: types.Message):
    await Student.first()


# @dp.message_handlers(state=Student.user_id)
async def log_user_answer_1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_id'] = message.from_user.id
    await Student.next()
    await message.answer("Выберите тип объекта")


# @dp.message_handlers(state=Student.type_of_object)
async def log_user_answer_2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['type_of_object'] = message.text
    await Student.next()
    await message.answer("Выберите название объекта")


# @dp.message_handlers(state=Student.name_of_object)
async def log_user_answer_3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_of_object'] = message.text
    await Student.next()
    await message.answer("Выберите дату, и время начала бронирования")


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
    await user_db.sql_booking(state)
    await state.finish()
    await message.answer("Переговорка забронирована")


def register_handlers_student(dp: Dispatcher):
    dp.register_message_handler(cmd_booking, commands=['booking'], state=None)
    dp.register_message_handler(log_user_answer_1, state=Student.user_id)
    dp.register_message_handler(log_user_answer_2, state=Student.type_of_object)
    dp.register_message_handler(log_user_answer_3, state=Student.name_of_object)
    dp.register_message_handler(log_user_answer_4, state=Student.start_time)
    dp.register_message_handler(log_user_answer_5, state=Student.end_time)
