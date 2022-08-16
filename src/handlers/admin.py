from aiogram import types, Dispatcher
from bookbot21.src.create_bot import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from bookbot21.src.databases import sql_database
from bookbot21.src.config import ADM_PASSWORD, STUDENT_PASSWORD, INTENSIVIST_PASSWORD

class AdmRoot(StatesGroup):
    name_for_object = State()
    type_for_object = State()
    description = State()
    campus_name = State()
    floor = State()
    number_of_room = State()
    photo = State()


# @dp.message_handler(commands=["add"], state=None)
async def cmd_add(message: types.Message):
    await message.answer("Введите название объекта")
    await AdmRoot.first()


@dp.message_handler(state=AdmRoot.name_for_object)
async def adm_answer_1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_for_object'] = message.text
        await AdmRoot.next()
        await message.answer("Введите тип объекта!")


@dp.message_handler(state=AdmRoot.type_for_object)
async def adm_answer_2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['type_for_object'] = message.text
        await AdmRoot.next()
        await message.answer("Введите описание!")


@dp.message_handler(state=AdmRoot.description)
async def adm_answer_3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
        await AdmRoot.next()
        await message.answer("Введите тип  кампус!")

@dp.message_handler(state=AdmRoot.campus_name)
async def adm_answer_4(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['campus_name'] = message.text
        await AdmRoot.next()
        await message.answer("Введите этаж!")


@dp.message_handler(state=AdmRoot.floor)
async def adm_answer_5(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['floor'] = message.text
        await AdmRoot.next()
        await message.answer("Введите номер кабинета !")


@dp.message_handler(state=AdmRoot.number_of_room)
async def adm_answer_6(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['number_of_room'] = message.text
        await AdmRoot.next()
        await message.answer("Загрузите фото!")


@dp.message_handler(state=AdmRoot.photo)
async def adm_answer_7(message: types.Messagem, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.text
        await message.answer("Вы успешно добавили!!!")
        state.finish()
