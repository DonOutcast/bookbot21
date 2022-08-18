from aiogram import types, Dispatcher
from src.create_bot import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from src.databases import sql_database
from src.config import ADM_PASSWORD, STUDENT_PASSWORD, INTENSIVIST_PASSWORD
from src.databases.init_database import user_db
from src.keyboards.inline_kb import city_markup, objects_markup
from src.keyboards.system_kb import back_menu_keyboard, keyboards_menu


class AdmRoot(StatesGroup):
    name_for_object = State()
    type_for_object = State()
    description = State()
    campus_name = State()
    floor = State()
    number_of_room = State()
    photo = State()


# user_db = sql_database.DatabaseBot("test1.db") #test1.db
# user_db.sql_create_users()
# user_db.sql_create_booking()
# user_db.sql_create_objects()




# @dp.message_handler(commands=["add"], state=None)
async def cmd_add(message: types.Message):
    rule = await user_db.sql_check_rule(message.from_user.id)
    if rule is None:
        await message.answer("Зарегистрируйтесь!")
    elif 'adm' in rule:
        await AdmRoot.first()
        await message.answer("Введите название объекта", reply_markup=back_menu_keyboard)
    else:
        await message.answer("Недостаточно прав! Обратитесь к ADM!")



# @dp.message_handler(state=AdmRoot.name_for_object)
async def adm_answer_1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_for_object'] = message.text.capitalize()
        await AdmRoot.next()
        await message.answer("Введите тип объекта!", reply_markup=objects_markup)


# @dp.callback_query_handler(Text(startswith='object_'), state=AdmRoot.type_for_object)
async def adm_answer_2(callback: types.CallbackQuery, state: FSMContext):
    object = callback.data.split('_')[1]
    async with state.proxy() as data:
        data['type_for_object'] = object
        await AdmRoot.next()
        await callback.answer()
        await callback.message.answer("Введите описание!")


# @dp.message_handler(state=AdmRoot.description)
async def adm_answer_3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
        await AdmRoot.next()
        await message.answer("Введите кампус!", reply_markup=city_markup)


# @dp.callback_handler(state=AdmRoot.campus_name)
async def adm_answer_4(callback: types.CallbackQuery, state: FSMContext):
    city = callback.data.split('_')[1]
    async with state.proxy() as data:
        data['campus_name'] = city
        await AdmRoot.next()
        await callback.answer()
        await callback.message.answer("Введите этаж!")


# @dp.message_handler(state=AdmRoot.floor)
async def adm_answer_5(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['floor'] = message.text
        await AdmRoot.next()
        await message.answer("Введите номер кабинета!")


# @dp.message_handler(state=AdmRoot.number_of_room)
async def adm_answer_6(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['number_of_room'] = message.text
        await AdmRoot.next()
        await message.answer("Загрузите фото!")


# @dp.message_handler(state=AdmRoot.photo)
async def adm_answer_7(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await user_db.sql_add_objects(state)
    # await user_db.sql_output(message)
    await message.answer("Вы успешно добавили!!!", reply_markup=keyboards_menu)
    await state.finish()


def register_handlers_adm(dp : Dispatcher):
    dp.register_message_handler(cmd_add, lambda message: 'Добавление 👨🏻‍💻' in message.text, state=None)
    dp.register_message_handler(adm_answer_1, state=AdmRoot.name_for_object)
    dp.register_callback_query_handler(adm_answer_2, Text(startswith='object_'), state=AdmRoot.type_for_object)
    dp.register_message_handler(adm_answer_3, state=AdmRoot.description)
    dp.register_callback_query_handler(adm_answer_4, Text(startswith='city_'), state=AdmRoot.campus_name)
    dp.register_message_handler(adm_answer_5, state=AdmRoot.floor)
    dp.register_message_handler(adm_answer_6, state=AdmRoot.number_of_room)
    dp.register_message_handler(adm_answer_7, content_types=['photo'], state=AdmRoot.photo)

