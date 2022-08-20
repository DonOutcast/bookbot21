from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


filter_list = CallbackData('type', 'action', 'id')


def check_rule(rule, list_types):
    if rule[0] == 'student':
        for price in list_types:
            if price[0] == 'игра':
                list_types.remove(price)
    elif rule[0] == 'intensivist':
        for price in list_types:
            if price[0] == 'игра':
                list_types = price,
    return list_types


async def inline_type_list(user_db, id):
    rule = await user_db.sql_check_rule(id)
    list_types = await user_db.sql_object_type(id)
    ret = len(list_types) != 0
    print("inline_type_list", list_types)
    list_types = check_rule(rule, list_types)
    row_button = []
    for type_name in list_types:
        line = InlineKeyboardButton(text=type_name[0],
                                    callback_data=filter_list.new(action='get_type_list',
                                                                  id=type_name[0]))
        row_button.append([line, ])
    return InlineKeyboardMarkup(inline_keyboard=row_button), ret


async def inline_object_list(user_db, type_name):
    list_object = await user_db.sql_list_object(type_name)
    print("inline_object_list", list_object)
    row_button = []
    for object_id, object_name in list_object:
        line = InlineKeyboardButton(text=object_name,
                                    callback_data=filter_list.new(action='get_object_list',
                                                                  id=object_name))
        row_button.append([line, ])
    return InlineKeyboardMarkup(inline_keyboard=row_button)
