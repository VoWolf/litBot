from telebot import types
from modules.instances.bot_instance import bot


def change_data(message, field_name, success_route, user_message):
    time_help = []

    bttns = types.InlineKeyboardMarkup(row_width=2)
    user_message = message.text
    btn1 = types.InlineKeyboardButton(
        "Да", callback_data=f"edit, yes, {time_help[2]}, {success_route}"
    )
    btn2 = types.InlineKeyboardButton(
        "Нет", callback_data=f"edit, no, {time_help[2]}, {success_route}"
    )
    bttns.add(btn1, btn2)
    alarm = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(
        "К кружку", callback_data=f"{time_help[2]} 0%#admin"
    )
    btn2 = types.InlineKeyboardButton(
        "Повторить попытку", callback_data=f"edit, time, {time_help[2]}"
    )
    btn3 = types.InlineKeyboardButton(
        "К списку кружков", callback_data="all_positions, page_1, remember"
    )
    alarm.add(btn1, btn2, btn3)
    c = message.text
    err = False
    if success_route == "time":
        if "$" not in c:
            if len(message.text.split()) >= 2:
                if len(message.text.split()[0].split("-")) >= 2:
                    c = f'\nВремя начала: {message.text.split()[0].split("-")[0]}\nВремя окончания: {message.text.split()[0].split("-")[1]}\nДень недели: {message.text.split()[1]}'
                else:
                    err = True
                    bot.send_message(
                        message.chat.id,
                        f'Данные указаны неверно! Ошибка: Missed {2 - len(message.text.split()[0].split("-"))} args* in >>[time start]-[time end]<< Пример: ([Время начала]-[Время окончания] [День недели в дательном падеже и мн. числе])',
                        reply_markup=alarm,
                    )
            else:
                err = True
                bot.send_message(
                    message.chat.id,
                    f"Данные указаны неверно! Ошибка: Missed {2 - len(message.text.split())} args* in message. Пример: ([Время начала]-[Время окончания] [День недели в дательном падеже и мн. числе])",
                    reply_markup=alarm,
                )
        else:
            if len(message.text.split()) >= 4:
                if len(message.text.split()[1].split("-")) >= 2:
                    if len(message.text.split()[2].split("-")) >= 2:
                        c = f"""\n1 группа:\nВремя начала: {message.text.split()[1].split("-")[0]}\nВремя окончания: {message.text.split()[1].split("-")[1]}\n2 группа:\nВремя начала: {message.text.split()[2].split("-")[0]}\nВремя окончания: {message.text.split()[2].split("-")[1]}\nДень недели: {message.text.split()[3]}"""
                    else:
                        err = True
                        bot.send_message(
                            message.chat.id,
                            f'ERROR: missed {2 - len(message.text.split()[2].split("-"))} args* Вы должны следовать данной схеме: ($ [Время начала занятий 1-й группы]-[Время окончания занятий 1-й группы] [Время начала занятий 2-й группы]-[Время окончания занятий 2-й группы] [День недели в дательном падеже])',
                            reply_markup=alarm,
                        )
                else:
                    err = True
                    bot.send_message(
                        message.chat.id,
                        f'ERROR: missed {2 - len(message.text.split()[1].split("-"))} args* Вы должны следовать данной схеме: ($ [Время начала занятий 1-й группы]-[Время окончания занятий 1-й группы] [Время начала занятий 2-й группы]-[Время окончания занятий 2-й группы] [День недели в дательном падеже])',
                        reply_markup=alarm,
                    )
            else:
                err = True
                bot.send_message(
                    message.chat.id,
                    f"ERROR: missed {4 - len(message.text.split())} args* Вы должны следовать данной схеме: ($ [Время начала занятий 1-й группы]-[Время окончания занятий 1-й группы] [Время начала занятий 2-й группы]-[Время окончания занятий 2-й группы] [День недели в дательном падеже])",
                    reply_markup=alarm,
                )
    if not err:
        bot.send_message(
            message.chat.id,
            f"New {field_name}: {c}. Подтвердить изменения?",
            reply_markup=bttns,
        )
