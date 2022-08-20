from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from prototype.admin.admin import user_db

filter_list_time = CallbackData('time', 'type', 'date', 'first_time', 'last_time')


async def time_list(date, object_id, first=True):
    res = await user_db.sql_check_booking(date, object_id)
    res_list = []

    for start, finish in res:
        start_h, start_m = map(int, start.split('.'))
        finish_h, finish_m = map(int, finish.split('.'))

        line_list = []
        for h in range(start_h, finish_h + 1):
            if h == start_h:
                if h == finish_h:
                    for m in range(start_m, finish_m + 15, 15):
                        line_list.append(f'{h}.{m:0<2}')
                else:
                    for m in range(start_m, 60, 15):
                        line_list.append(f'{h}.{m:0<2}')
            elif h == finish_h:
                for m in range(0, finish_m + 15, 15):
                    line_list.append(f'{h}.{m:0<2}')
            else:
                for m in range(0, 60, 15):
                    line_list.append(f'{h}.{m:0<2}')

        if first:
            line_list = line_list[:-1]
        else:
            line_list = line_list[1:]
        res_list.extend(line_list)

    return res_list


async def get_time(date, object_id, start_time=None):
    if start_time is not None:
        t_list = await time_list(date, object_id, first=False)
        start_hour, start_minute = map(int, start_time.split('.'))
        start_minute += 15
    else:
        t_list = await time_list(date, object_id)
        start_hour, start_minute = 0, 0

    list_time = []
    for hour in range(start_hour, 24):
        for minute in range(start_minute, 60, 15):
            list_time.append(f'{hour}.{minute:0<2}')
        start_minute = 0

    line = []
    res_list = []
    flag = False
    for i, str_time in enumerate(list_time):
        if str_time in t_list:
            if start_time is not None:
                flag = True
                break
            line.append(InlineKeyboardButton(text='.',
                                             callback_data='.'))
        else:
            print("IN inline", object_id)
            line.append(InlineKeyboardButton(text=str_time,
                                             callback_data=filter_list_time.new(
                                                 type=('first' if start_time is None else 'last'),
                                                 date=date,
                                                 first_time=(str_time if start_time is None else start_time),
                                                 last_time=(str_time if start_time is not None else '.'))
                                             )
                        )

        if len(line) == 4:
            res_list.append(line)
            line = []

        if flag:
            break
    res_list.append(line)

    return InlineKeyboardMarkup(inline_keyboard=res_list)
