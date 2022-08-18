from aiogram import types, Dispatcher
from src.create_bot import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from src.databases import sql_database
from src.config import ADM_PASSWORD, STUDENT_PASSWORD, INTENSIVIST_PASSWORD
from src.handlers.admin import user_db
from src.my_calendar.inline_calendar import get_date, filter_list_date
from src.my_calendar.inline_time_list import get_time, filter_list_time
from src.keyboards.system_kb import back_menu_keyboard


class Student(StatesGroup):
    user_id = State()
    description = State()
    # check_rule = State()
    type_of_object = State()
    name_of_object = State()
    object_id = State()
    user_date = State()
    # start_time = State()
    # end_time = State()


# @dp.message_handlers(commands=['/booking'], state=None)
async def cmd_booking(message: types.Message, state: FSMContext):
    await Student.first()
    async with state.proxy() as data:
        data['user_id'] = message.from_user.id
    await Student.next()
    await message.answer("Введите описание мероприятия", reply_markup=back_menu_keyboard)


# @dp.message_handlers(state=Student.description)
async def log_user_answer_1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await Student.next()
    await message.answer("Выберите тип объекта")
    rule = await user_db.sql_check_rule(message.from_user.id)
    # if "".join(rule) == 'adm':
    #     await message.answer("Game")


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


# @dp.message_handler(state=Student.name_of_object)
async def log_user_answer_3(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['name_of_object'] = message.text
    await Student.next()
    object_id = await user_db.sql_get_id(state)
    if object_id:
        async with state.proxy() as data:
            data['object_id'] = object_id[0]
        await Student.next()
        await message.answer("Выберите дату", reply_markup=await get_date())
    else:
        await state.finish()
        await message.answer("Соряян")

# # @dp.message_handler(state=Student.object_id)
# async def checking_object_id(message: types.Message, state: FSMContext):
#     object_id = await user_db.sql_get_id(state)
#     )

# @dp.callback_query_handler(filter_list_date.filter(type='refresh'))
async def enter_test_1(callback_query: types.CallbackQuery, callback_data: dict):
    await callback_query.answer()
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=callback_query.message.text,
        reply_markup=get_date(callback_data['date']))


# # @dp.message_handler(state=Student.user_date)
# async def log_user_answer_date(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['user_data'] = message.text
#     await Student.next()
#     await message.answer("Выберите время начала бронирования")


# @dp.message_handler(state=Student.user_date)
async def check_choice_date(message: types.Message):
    await message.delete()
    await message.answer("Выберите нужную вам дату(время) из календаря")


# @dp.callback_query_handler(filter_list_date.filter(type='get_date'))
async def enter_test_2(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.delete()
    date = callback_data.get("date")
    async with state.proxy() as data:
        object_id = data['object_id']
    await callback_query.message.answer(text=f'Дата: {date}\nВыберите время начала',
                                        reply_markup=await get_time(date=date,
                                                                    object_id=object_id))


# @dp.callback_query_handler(filter_list_time.filter(type='first'))
async def enter_test_3(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        object_id = data['object_id']
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=callback_query.message.text.replace('Выберите время начала', 'Выберите время конца'),
        reply_markup=await get_time(date=callback_data['date'], start_time=callback_data['first_time'], object_id=object_id))


# @dp.callback_query_handler(filter_list_time.filter(type='last'))
async def enter_test_4(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.delete()
    date = callback_data['date']
    start_time = callback_data['first_time']
    end_time = callback_data['last_time']
    async with state.proxy() as data:
        data = tuple(data.values())
    print("callback_data", callback_data)
    data = (*data, date, start_time, end_time)
    query = await user_db.sql_booking(data)
    await state.finish()
    if query:
        login = await user_db.sql_get_login(callback_query.from_user.id)
        await callback_query.message.answer(f"Вы {login[0]} успешно забранировали!")
        await user_db.sql_my_booking(callback_query.from_user.id, False)
    else:
        await callback_query.message.answer(text="Ощибка бронирования")

# # @dp.message_handler(state=Student.user_date)
# async def log_user_answer_date(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['user_data'] = message.text
#     await Student.next()
#     await message.answer("Выберите время начала бронирования")
#
# # @dp.message_handlers(state=Student.start_time)
# async def log_user_answer_4(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['start_time'] = message.text
#     await Student.next()
#     await message.answer("Выберите дату , время конца бронирования")
#
#
# # @dp.message_handlers(state=Student.start_time)
# async def log_user_answer_5(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['end_time'] = message.text
#     query = await user_db.sql_booking(data)
#     await state.finish()
#     if query:
#         login = await user_db.sql_get_login(message.from_user.id)
#         await message.answer(f"Вы {login[0]} успешно забранировали!")
#         await user_db.sql_my_booking(message.from_user.id, False)
#     else:
#         await bot.send_message(message.from_user.id, text="Ощибка бронирования")


# @dp.callback_query_handler(Text(equals="cancel_calendar"), state=Student.user_date)
async def remove_calendar(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback_query.message.delete()


def register_handlers_student(dp: Dispatcher):
    dp.register_message_handler(cmd_booking, lambda message: 'Бронирование ✅' in message.text, state=None)
    dp.register_message_handler(log_user_answer_1, state=Student.description)
    dp.register_message_handler(log_user_answer_2, state=Student.type_of_object)
    # dp.register_message_handler(log_user_answer_date, state=Student.user_date)
    dp.register_message_handler(log_user_answer_3, state=Student.name_of_object)
    # dp.register_message_handler(checking_object_id, state=Student.object_id)
    dp.register_callback_query_handler(enter_test_1, filter_list_date.filter(type='refresh'), state=Student.user_date)
    dp.register_callback_query_handler(remove_calendar, Text(equals="cancel_calendar"), state=Student.user_date)
    dp.register_message_handler(check_choice_date, state=Student.user_date)
    dp.register_callback_query_handler(enter_test_2, filter_list_date.filter(type='get_date'), state=Student.user_date)
    dp.register_callback_query_handler(enter_test_3, filter_list_time.filter(type='first'), state=Student.user_date)
    dp.register_callback_query_handler(enter_test_4, filter_list_time.filter(type='last'), state=Student.user_date)
    # dp.register_message_handler(log_user_answer_4, state=Student.start_time)
    # dp.register_message_handler(log_user_answer_5, state=Student.end_time)

