from telebot import types
from modules.utils.db_utils import change_data
from modules.controllers.street_controller import process_street
from modules.controllers.page_controller import PageSwitcher


page = None


page_message_data = 0


def main_handler(call, bot):
    """Handles main route"""
    bttns = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(
        "Дополнительное образование", callback_data="dop_education"
    )
    btn2 = types.InlineKeyboardButton("Контактные данные", callback_data="contacts")
    bttns.add(btn1, btn2)
    bot.send_message(
        call.message.chat.id,
        "Здравствуйте! Я бот Лицея №1533 и могу ответить на ваши вопросы. Ниже представлены разделы, которые в меня "
        "загружены. Если вам нужна помощь воспользуйтесь командой /help.",
        reply_markup=bttns,
    )


def contacts_handler(call, bot):
    """Handles contacts"""
    markup = types.InlineKeyboardMarkup(row_width=1)
    item = types.InlineKeyboardButton(
        "Корпуса на карте",
        url="https://yandex.ru/maps/213/moscow/?ll=37.555258%2C55.691771&mode=usermaps&um=constructor"
            "%3A1nzJdcg6iOPjfPFPXyh90u3R46dsk_8W&z=15",
    )
    item2 = types.InlineKeyboardButton(
        "Официальный сайт", url="https://lyc1533.mskobr.ru/"
    )
    item3 = types.InlineKeyboardButton(
        "Содружество лицея", url="https://www.lit.msu.ru/"
    )
    markup.row(item2, item3)
    item4 = types.InlineKeyboardButton("Главная", callback_data="main")
    item5 = types.InlineKeyboardButton("Каникулы", callback_data="holidays")
    markup.row(item4, item5)
    bot.send_message(
        call.message.chat.id,
        "Звоните с 9 до 18 часов в учебное время, а также с 10 до 16 во время каникул: \n +7 499 133-24-35 ... "
        "Ломоносовский, \n +7 499 124-55-65 ... Профсоюзная, \n +7 499 125-23-59 ... Кржижановского",
        reply_markup=markup,
    )


def admin_page_handler(call, bot):
    """Handler for admin"""
    bttns = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(
        "Изменить список/структуру кружков",
        callback_data="all_positions, page 1, remember",
    )
    btn2 = types.InlineKeyboardButton(
        "Изменить пароль администратора", callback_data="change_password"
    )
    btn3 = types.InlineKeyboardButton("Выйти из аккаунта", callback_data="logout")
    bttns.add(btn1, btn2, btn3)
    bot.send_message(
        call.message.chat.id,
        "Вы на главной странице администратора!",
        reply_markup=bttns,
    )


def how_to_register_handler(call, bot):
    """Handler for registration"""
    bttns = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("Обратно", callback_data="contacts")
    btn2 = types.InlineKeyboardButton("К выбору кружка", callback_data="dop_education")
    bttns.add(btn, btn2)
    bot.send_message(
        call.message.chat.id,
        'Это делается через сайт mos.ru. Вот подробная инструкция по записи:\n1. Зайдите на сайт mos.ru и войдите '
        'в аккаунт\n2. Сверху перечислены разделы, перейдите в раздел "услуги"\n3. В меню слева выбираете услугу '
        '"образование". Если ее не видно, воспользуйтесь строкой для поиска\n4. Когда вы выберете услугу "образование",'
        ' чуть правее появится выбор раздела. Выберите "допобразование"\n5. Еще правее выберите пункт "Запись в кружки,'
        ' спортивные секции, дома творчества", нажмите на него\n6. Подтвердите свой выбор, нажав на кнопку "Получить '
        'услугу"\n7. В открывшемся окне выберите пункт "Запись в кружок", ниже введите код кружка (его можно получить в'
        ' этом боте)\n8. Далее следуйте инструкциям на сайте, удачи! ВАЖНО! Для записи к Вашему аккаунту на mos.ru '
        'должен быть привязан СНИЛС ',
        reply_markup=bttns,
    )


def dop_education_handler(call, bot):
    """Additional education handler"""
    bttns = types.InlineKeyboardMarkup()
    bttns.row(
        types.InlineKeyboardButton(
            "На Профсоюзной", callback_data="Look_at_education_in, remember, profsoyuznaya"
        ),
        types.InlineKeyboardButton(
            "На Ломоносовском", callback_data="Look_at_education_in, remember, lomonosovsky"
        )
    )
    bttns.row(
        types.InlineKeyboardButton(
            "На Крижановского", callback_data="Look_at_education_in, remember, krzhizhanovskogo"
        ),
        types.InlineKeyboardButton(
            "Все наши кружки", callback_data="all_positions, page_1, remember"
        )
    )
    bttns.row(
        types.InlineKeyboardButton(
            "Главная", callback_data="main"
        )
    )

    bot.send_message(
        call.message.chat.id, "Кружки в каком корпусе вас интересуют?", reply_markup=bttns
    )
    bttns.row(
        types.InlineKeyboardButton(
            "Главная", callback_data="main"
        )
    )


def position_details_handler(call, bot, admin, db):
    bttns = types.InlineKeyboardMarkup(row_width=2)
    btn0 = types.InlineKeyboardButton(
        "К кружкам", callback_data="all_positions, page_1, remember"
    )
    btn1 = types.InlineKeyboardButton("Главная", callback_data="main")
    bttns.row(btn0, btn1)
    result = db.execute(
        """SELECT * FROM dop_ed WHERE id = ?""", (call.data.split()[0],)
    ).fetchone()
    if admin:
        btn1 = types.InlineKeyboardButton(
            "Название", callback_data=f"edit, name, {result[0]}"
        )
        btn2 = types.InlineKeyboardButton(
            "Доступные классы", callback_data=f"edit, klass, {result[0]}"
        )
        btn3 = types.InlineKeyboardButton(
            "Имя преподавателя", callback_data=f"edit, teacher_name, {result[0]}"
        )
        btn4 = types.InlineKeyboardButton(
            "Время проведения", callback_data=f"edit, time, {result[0]}"
        )
        btn5 = types.InlineKeyboardButton(
            "Аудиторию", callback_data=f"edit, aud, {result[0]}"
        )
        if result[-4] == "-":
            btn6 = types.InlineKeyboardButton(
                "Сделать платным",
                callback_data=f"edit, do_plat_yes, {result[0]}",
            )
        else:
            btn6 = types.InlineKeyboardButton(
                "Сделать бесплатным",
                callback_data=f"edit, do_plat_no, {result[0]}",
            )
        btn7 = types.InlineKeyboardButton(
            "Дату старта", callback_data=f"edit, start_date, {result[0]}"
        )
        if result[9] == "+":
            btn8 = types.InlineKeyboardButton(
                "Код для записи", callback_data=f"edit, kode, {result[0]}"
            )
            bttns.add(btn8)
            btn9 = types.InlineKeyboardButton(
                "Скрыть код", callback_data=f"edit, remove_kode, {result[0]}"
            )
        else:
            btn9 = types.InlineKeyboardButton(
                "Показать код", callback_data=f"edit, show_kode, {result[0]}"
            )
        btn10 = types.InlineKeyboardButton(
            "Изменить тип", callback_data=f"edit, type, {result[0]}"
        )
        btn11 = types.InlineKeyboardButton(
            "Удалить запись", callback_data=f"edit, remove, {result[0]}"
        )
        btn12 = types.InlineKeyboardButton(
            "Корпус", callback_data=f"edit, korp, {result[0]}"
        )
        btn13 = types.InlineKeyboardButton(
            "Категорию", callback_data=f"edit, type, {result[0]}, 0"
        )
        bttns.add(
            btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn9, btn10, btn11, btn12, btn13
        )
        if result[0] > 10000:
            bttns.add(
                types.InlineKeyboardButton(
                    "PUSH", callback_data=f"edit, push, {result[0]}"
                )
            )
        else:
            bttns.add(
                types.InlineKeyboardButton(
                    "TAKE", callback_data=f"edit, take, {result[0]}"
                )
            )

    ans = ""

    help = str(result[2]).split()
    if len(help) > 1:
        ans += f"{result[1]} для {', '.join(str(result[2]).split()[0:-1])} и {str(result[2]).split()[-1]} классов на {result[-1]}:\n\n"
    else:
        ans += f"{result[1]} для {', '.join(str(result[2]).split())} классов:\n"
    ans += f"Преподаватель: {result[5]}\n"
    time = result[6].split()
    if "$" not in time:
        startend = time[0].split("-")
        start = startend[0]
        end = startend[1]
        ans += f"Проходит с {start} до {end}, по {time[1]}\n"
    else:
        del time[0]
        ans += f'Имеется 2 группы: \n1 группа: с {time[0].split("-")[0]} до {time[0].split("-")[1]}\n2 группа: с {time[1].split("-")[0]} до {time[1].split("-")[1]}\nПо {time[2]}\n'
    ans += f"Аудитория: {result[7]}\n"
    if result[-4] == "+":
        ans += "Данный кружок является платным!\n"
    if result[-2] != "-":
        ans += f"Данный кружок начинается {result[-2]}"
    if result[9] == "+":
        ans += f"\nКод для записи на mos.ru: <code>{result[4]}</code> (нажмите чтобы скопировать)"
    else:
        ans += "Данный кружок не требует записи на mos.ru"
    if admin:
        bot.send_message(
            call.message.chat.id,
            f"{ans}\n\nЧто хотите изменить?",
            parse_mode="HTML",
            reply_markup=bttns,
        )
    else:
        bot.send_message(
            call.message.chat.id, ans, parse_mode="HTML", reply_markup=bttns
        )


def all_positions_handler(call, bot, admin, db):
    global page_message_data

    if "remember" in call.data:
        page_message_data = call.message.id

    if "page_1" in call.data:
        # empty shows True if buttons exist and False if not
        buttons = empty = process_street(admin, db, "profsoyuznaya")
        if not buttons:
            buttons = types.InlineKeyboardMarkup(row_width=2)
        buttons.row(
            types.InlineKeyboardButton("На стр. 2", callback_data="all_positions, page_2")
        )
        if empty:
            bot.edit_message_text(
                'Страница 1/3:\n<u><b>Профсоюзная</b></u> // Ломоносовский // Крижановского\nВсе кружки на Профсоюзной:',
                call.message.chat.id, page_message_data, parse_mode='HTML', reply_markup=buttons
            )
        else:
            bot.edit_message_text(
                'Страница 1/3:\n<u><b>Профсоюзная</b></u> // Ломоносовский // Крижановского\nК сожалению, кружков на Профсоюзной пока что не добавлено! Для актуальной информации обратитесь к разделу "наша учеба" на сайте www.lit.msu.ru',
                call.message.chat.id, page_message_data, parse_mode='HTML', reply_markup=buttons
            )

    elif "page_2" in call.data:
        buttons = empty = process_street(admin, db, "lomonosovsky")
        if not buttons:
            buttons = types.InlineKeyboardMarkup(row_width=2)
        buttons.row(
            types.InlineKeyboardButton("На стр. 1", callback_data="all_positions, page_1"),
            types.InlineKeyboardButton("На стр. 3", callback_data="all_positions, page_3")
        )
        if empty:
            bot.edit_message_text(
                'Страница 2/3:\nПрофсоюзная // <u><b>Ломоносовский</b></u> // Крижановского\nВсе кружки на Ломоносовском:',
                call.message.chat.id, page_message_data, parse_mode='HTML', reply_markup=buttons
            )
        else:
            bot.edit_message_text(
                'Страница 2/3:\nПрофсоюзная // <u><b>Ломоносовский</b></u> // Крижановского\nК сожалению, кружков на Ломоносовском пока что не добавлено! Для актуальной информации обратитесь к разделу "наша учеба" на сайте www.lit.msu.ru',
                call.message.chat.id, page_message_data, parse_mode='HTML', reply_markup=buttons
            )

    elif "page_3" in call.data:
        buttons = empty = process_street(admin, db, "krzhizhanovskogo")
        if not buttons:
            buttons = types.InlineKeyboardMarkup(row_width=2)
        buttons.row(
            types.InlineKeyboardButton("На стр. 2", callback_data="all_positions, page_2"),
        )
        if empty:
            bot.edit_message_text(
                'Страница 3/3:\nПрофсоюзная // Ломоносовский // <u><b>Крижановского</b></u>\nВсе кружки на Крижановского:',
                call.message.chat.id, page_message_data, parse_mode='HTML', reply_markup=buttons
            )
        else:
            bot.edit_message_text(
                'Страница 3/3:\nПрофсоюзная // Ломоносовский // <u><b>Крижановского</b></u>\nК сожалению, кружков на Крижановского пока что не добавлено! Для актуальной информации обратитесь к разделу "наша учеба" на сайте www.lit.msu.ru',
                call.message.chat.id, page_message_data, parse_mode='HTML', reply_markup=buttons
            )


def look_at_education_handler(call, bot, admin, db):
    """Additional education handler"""
    global page
    if call.data.split(", ")[1] == "remember":
        page = PageSwitcher(street_name=call.data.split()[2], admin=admin, db=db, message_id=call.message.id)
        buttons, text = page.start_page()
        if len(page.page_buttons) == 1:
            bot.edit_message_text(f"К сожалению, кружков на {page.street_russian_name} пока что не добавлено! "
                                  f"Пожалуйта, обратитесь к разделу 'Наша учеба' на сайте www.lit.msu.ru (Сообществе "
                                  f"лицея) или свяжитесь с администрацией!", call.message.chat.id, page.message_id,
                                  reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(
                                      "Главная", callback_data="main"))
                                  )
        else:
            bot.edit_message_text(text, call.message.chat.id, page.message_id, reply_markup=buttons, parse_mode="HTML")
    if call.data.split(", ")[1] == "prev_page":
        buttons, text = page.prev_page()
        bot.edit_message_text(text, call.message.chat.id, page.message_id, reply_markup=buttons, parse_mode="HTML")
    elif call.data.split(", ")[1] == "next_page":
        print(page)
        buttons, text = page.next_page()
        bot.edit_message_text(text, call.message.chat.id, page.message_id, reply_markup=buttons, parse_mode="HTML")


def holidays_handler(bot, call):
    buttons = types.InlineKeyboardMarkup()
    buttons.row(
        types.InlineKeyboardButton(
            "Главная", callback_data="main"
        ),
        types.InlineKeyboardButton(
            "Назад", callback_data="contacts"
        )
    )
    file = open("./holidays_2023-2024.png", "rb")
    bot.send_photo(call.message.chat.id, file, 'Расписание каникул на 2023 - 2024 год!', reply_markup=buttons)
    file.close()


def edit_handler(call, bot, db, connection):
    message_text = ""

    time_help = call.data.split(", ")
    bttns = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("К списку админа", callback_data="admin")
    btn2 = types.InlineKeyboardButton(
        "К списку Кружков", callback_data="all_positions, page_1, remember"
    )
    btn3 = types.InlineKeyboardButton(
        "К кружку", callback_data=f"{time_help[2]} position_details"
    )
    bttns.add(btn1, btn2, btn3)

    if "teacher_name" in call.data:
        if "yes" in call.data:
            db.execute(
                """UPDATE dop_ed SET teacher = ? WHERE id = ?""",
                (message_text, time_help[2]),
            )
            connection.commit()
            bot.send_message(
                call.message.chat.id,
                f'Данные успешно внесены! Новое имя пеподавателя: <code>{"".join([el for el in db.execute("SELECT teacher FROM dop_ed WHERE id = ?", (time_help[2],)).fetchone()[0]])}</code>',
                reply_markup=bttns,
                parse_mode="HTML",
            )
        elif "no" in call.data:
            bot.send_message(
                call.message.chat.id, "Изменения не применены!", reply_markup=bttns
            )
        else:
            bot.send_message(
                call.message.chat.id,
                f'Текущее имя учителя: <code>{" ".join([el[0] for el in db.execute("SELECT teacher FROM dop_ed WHERE id=?", (time_help[2],))])}</code>\nНовое имя ниже',
                parse_mode="HTML",
            )
            bot.register_next_step_handler(
                call.message, change_data, "имя учителя", "teacher_name", message_text
            )
    elif "name" in call.data:
        if "yes" in call.data:
            db.execute(
                """UPDATE dop_ed SET name = ? WHERE id = ?""",
                (message_text, time_help[2]),
            )
            connection.commit()
            bot.send_message(
                call.message.chat.id,
                f'Данные успешно внесены! Новое название: <code>{"".join([el for el in db.execute("SELECT name FROM dop_ed WHERE id = ?", (time_help[2],)).fetchone()[0]])}</code>',
                reply_markup=bttns,
                parse_mode="HTML",
            )
        elif "no" in call.data:
            bot.send_message(
                call.message.chat.id, "Изменения не применены!", reply_markup=bttns
            )
        else:
            bot.send_message(
                call.message.chat.id,
                f'Текущее имя: <code>{" ".join([el[0] for el in db.execute("SELECT name FROM dop_ed WHERE id=?", (time_help[2],))])}</code>\nНовое имя введите ниже',
                parse_mode="HTML",
            )
            bot.register_next_step_handler(
                call.message, change_data, "имя", "name", message_text
            )
    elif "klass" in call.data:
        if "yes" in call.data:
            db.execute(
                """UPDATE dop_ed SET klasses = ? WHERE id = ?""",
                (message_text, time_help[2]),
            )
            connection.commit()
            bot.send_message(
                call.message.chat.id,
                f'Данные успешно внесены! Классы, которым можно посещаять занятия: <code>{", ".join([str(el) for el in db.execute("SELECT klasses FROM dop_ed WHERE id = ?", (time_help[2],)).fetchone()[0]])}</code>',
                reply_markup=bttns,
                parse_mode="HTML",
            )
        elif "no" in call.data:
            bot.send_message(
                call.message.chat.id, "Изменения не применены!", reply_markup=bttns
            )
        else:
            bot.send_message(
                call.message.chat.id,
                f'Текущее значение допускаемых классов: <code>{" ".join([str(el[0]) for el in db.execute("SELECT klasses FROM dop_ed WHERE id=?", (time_help[2],))])}</code>\nНовое значение введите ниже',
                parse_mode="HTML",
            )
            bot.register_next_step_handler(
                call.message, change_data, "значения", "klass", message_text
            )
    elif "time" in call.data:
        if "yes" in call.data:
            db.execute(
                """UPDATE dop_ed SET time = ? WHERE id = ?""",
                (message_text, time_help[2]),
            )
            connection.commit()
            bot.send_message(
                call.message.chat.id, "Данные успешно внесены!", reply_markup=bttns
            )
        elif "no" in call.data:
            bot.send_message(
                call.message.chat.id, "Изменения не применены!", reply_markup=bttns
            )
        else:
            time = db.execute(
                """SELECT time FROM dop_ed WHERE id = ?""", (time_help[2],)
            ).fetchall()[0][0]
            time = time.split()
            if "$" not in time:
                start = time[0].split("-")[0]
                end = time[0].split("-")[1]
                bot.send_message(
                    call.message.chat.id,
                    f" Текущее время проведения: \nВремя начала: <code>{start}</code> \nВремя окончания: <code>{end}</code> \nДень недели (проведения): <code>{time[1]}</code> \nНовое значение введите ниже в формате ([время начала]-[время окончания] [день недели в дательном падеже]). Если хотите изменить время проведения по группам (Группа 1, группа 2), то воспользуйтесь другим форматом: ($ [Время начала занятий 1-й группы]-[Время окончания занятий 1-й группы] [Время начала занятий 2-й группы]-[Время окончания занятий 2-й группы] [День недели в дательном падеже]):",
                    parse_mode="HTML",
                )
            else:
                del time[0]
                gr_1_start = time[0].split("-")[0]
                gr_1_end = time[0].split("-")[1]
                gr_2_start = time[1].split("-")[0]
                gr_2_end = time[1].split("-")[1]
                bot.send_message(
                    call.message.chat.id,
                    f"Текущее время проведения: \n1 группа: с {gr_1_start} до {gr_1_end}\n2 группа: с {gr_2_start} до {gr_2_end}\nПо {time[2]}. \nНовое значение введите ниже в формате ([время начала]-[время окончания] [день недели в дательном падеже]). Если хотите изменить время проведения по группам (Группа 1, группа 2), то воспользуйтесь другим форматом: ($ [Время начала занятий 1-й группы]-[Время окончания занятий 1-й группы] [Время начала занятий 2-й группы]-[Время окончания занятий 2-й группы] [День недели в дательном падеже]):",
                    parse_mode="HTML",
                )

            bot.register_next_step_handler(
                call.message, change_data, "время проведения", "time", message_text
            )
    elif "aud" in call.data:
        if "yes" in call.data:
            db.execute(
                """UPDATE dop_ed SET aud = ? WHERE id = ?""",
                (message_text, time_help[2]),
            )
            connection.commit()
            bot.send_message(
                call.message.chat.id,
                f'Данные успешно внесены! Аудитория изменена на <code>{"".join([el for el in db.execute("SELECT aud FROM dop_ed WHERE id = ?", (time_help[2],)).fetchone()[0]])}</code>',
                reply_markup=bttns,
                parse_mode="HTML",
            )
        elif "no" in call.data:
            bot.send_message(
                call.message.chat.id, "Изменения не применены!", reply_markup=bttns
            )
        else:
            bot.send_message(
                call.message.chat.id,
                f'Текущее место проведения: <code>{" ".join([el[0] for el in db.execute("SELECT aud FROM dop_ed WHERE id=?", (time_help[2],))])}</code>\nНовое место проведения занятий введите ниже',
                parse_mode="HTML",
            )
            bot.register_next_step_handler(
                call.message,
                change_data,
                "место проведения занятий",
                "aud",
                message_text,
            )
    elif "do_plat_yes" in call.data or "do_plat_no" in call.data:
        if "do_plat_yes" in call.data:
            db.execute(
                """UPDATE dop_ed SET plat = ? WHERE id = ?""", ("+", time_help[2])
            )
            bot.send_message(
                call.message.chat.id, "Кружок сделан платным!", reply_markup=bttns
            )
        else:
            db.execute(
                """UPDATE dop_ed SET plat = ? WHERE id = ?""", ("-", time_help[2])
            )
            bot.send_message(
                call.message.chat.id, "Кружок сделан бесплатным!", reply_markup=bttns
            )
        connection.commit()
    elif "start_date" in call.data:
        if "yes" in call.data:
            db.execute(
                """UPDATE dop_ed SET sinse = ? WHERE id = ?""",
                (message_text, time_help[2]),
            )
            connection.commit()
            bot.send_message(
                call.message.chat.id,
                f'Данные успешно внесены! Время старта занятий изменено на <code>{"".join([el for el in db.execute("SELECT sinse FROM dop_ed WHERE id = ?", (time_help[2],)).fetchone()[0]])}</code>',
                reply_markup=bttns,
                parse_mode="HTML",
            )
        elif "no" in call.data:
            bot.send_message(
                call.message.chat.id, "Изменения не применены!", reply_markup=bttns
            )
        else:
            if (
                    " ".join(
                        [
                            el[0]
                            for el in db.execute(
                            "SELECT sinse FROM dop_ed WHERE id=?", (time_help[2],)
                        )
                        ]
                    )
                    == "-"
            ):
                bot.send_message(
                    call.message.chat.id,
                    "Дата старта данного кружка не указана (=> стартует 1 сент.), новое значение укажите ниже:",
                )
            else:
                bot.send_message(
                    call.message.chat.id,
                    f'Текущая дата старта: <code>{" ".join([el[0] for el in db.execute("SELECT sinse FROM dop_ed WHERE id=?", (time_help[2],))])}</code>\nНовую дату старта укажите ниже (напишите "<code>-</code>" если дата старта 1 сентября):',
                    parse_mode="HTML",
                )
            bot.register_next_step_handler(
                call.message, change_data, "дата старта", "start_date", message_text
            )
            bot.register_next_step_handler(
                call.message, change_data, "значения", "klass", message_text
            )
    elif "remove_kode" in call.data or "show_kode" in call.data:
        if "remove_kode" in call.data:
            if "yes" in call.data:
                db.execute(
                    """UPDATE dop_ed SET reg = '-', code = '-' WHERE id = ?""",
                    (time_help[2],),
                )
                connection.commit()
                bot.send_message(
                    call.message.chat.id,
                    "Регистрация на данный кружок отменена!",
                    reply_markup=bttns,
                )
            elif "no" in call.data:
                bot.send_message(
                    call.message.chat.id, "Действия не применены!", reply_markup=bttns
                )
            else:
                cc = types.InlineKeyboardMarkup(row_width=1)
                btn1 = types.InlineKeyboardButton(
                    "Подтвердить действия",
                    callback_data=f"edit, remove_kode, {time_help[2]}, yes",
                )
                btn2 = types.InlineKeyboardButton(
                    "Не подтверждать действия",
                    callback_data=f"edit, remove_kode, {time_help[2]}, no",
                )
                db.add(btn1, btn2)
                bot.send_message(
                    call.message.chat.id,
                    f'Вы уверены что хотите отменить регистрацию на кружок {"".join([str(el) for el in db.execute("SELECT name FROM dop_ed WHERE id = ?", (time_help[2],)).fetchall()[0]])}? <b>Внимание!</b> При подтверждении действия текущий код (<code>{"".join([str(el) for el in db.execute("SELECT code FROM dop_ed WHERE id = ?", (time_help[2],)).fetchall()[0]])}</code>) будет стерт!',
                    parse_mode="HTML",
                    reply_markup=cc,
                )
        elif "show_kode" in call.data:
            if "yes" in call.data:
                db.execute(
                    """UPDATE dop_ed SET reg = '+', code = ? WHERE id = ?""",
                    (message_text, time_help[2]),
                )
                connection.commit()
                bot.send_message(
                    call.message.chat.id,
                    f"Регистрация на данный кружок введена. Новый код: <code>{message_text}</code>",
                    reply_markup=bttns,
                    parse_mode="HTML",
                )
            elif "no" in call.data:
                bot.send_message(
                    call.message.chat.id, "Действия не применены!", reply_markup=bttns
                )
            else:
                bot.send_message(
                    call.message.chat.id, f"Все почти готово! Ниже введите код кружка:"
                )
                bot.register_next_step_handler(
                    call.message, change_data, "код", "show_kode", message_text
                )
    elif "kode" in call.data:
        if "yes" in call.data:
            db.execute(
                """UPDATE dop_ed SET code = ? WHERE id = ?""",
                (message_text, time_help[2]),
            )
            connection.commit()
            bot.send_message(
                call.message.chat.id,
                f'Данные успешно внесены! Код сменен на <code>{"".join([str(el) for el in db.execute("SELECT code FROM dop_ed WHERE id = ?", (time_help[2],)).fetchone()[0]])}</code>',
                reply_markup=bttns,
                parse_mode="HTML",
            )
        elif "no" in call.data:
            bot.send_message(
                call.message.chat.id, "Изменения не применены!", reply_markup=bttns
            )
        else:
            bot.send_message(
                call.message.chat.id,
                f'Текущий код для записи: <code>{" ".join([str(el[0]) for el in db.execute("SELECT code FROM dop_ed WHERE id=?", (time_help[2],))])}</code>\nНовый код введите ниже',
                parse_mode="HTML",
            )
            bot.register_next_step_handler(
                call.message, change_data, "код для записи", "kode", message_text
            )
    elif "remove" in call.data:
        if "yes" in call.data:
            db.execute("""DELETE FROM dop_ed WHERE id = ?""", (time_help[2],))
            connection.commit()
            bot.send_message(
                call.message.chat.id,
                "Запись удалена!",
                reply_markup=types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton(
                        "К куржкам", callback_data="all_positions, page_1, remember"
                    )
                ),
            )
        elif "no" in call.data:
            bot.send_message(
                call.messae.chat.id,
                "Запись не удалена!",
                reply_markup=types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton(
                        "К куржкам", callback_data="all_positions, page_1, remember"
                    )
                ),
            )
        else:
            cc = types.InlineKeyboardMarkup(row_width=1)
            btn1 = types.InlineKeyboardButton(
                "Подтвердить действия",
                callback_data=f"edit, remove, {time_help[2]}, yes",
            )
            btn2 = types.InlineKeyboardButton(
                "Не подтверждать действия",
                callback_data=f"edit, remove, {time_help[2]}, no",
            )
            cc.add(btn1, btn2)
            bot.send_message(
                call.message.chat.id,
                f'Вы уверены что хотите удалить запись о {"".join([str(el[0]) for el in db.execute("SELECT name FROM dop_ed WHERE id = ?", (time_help[2],)).fetchall()])}? <b>ОНА БУДЕТ БЕЗВОЗВРАТНО УТЕРЯНА</b>',
                parse_mode="HTML",
                reply_markup=cc,
            )
    elif "korp" in call.data:
        if "yes" in call.data:
            db.execute(
                """UPDATE dop_ed SET korp = ? WHERE id = ?""",
                (message_text, time_help[2]),
            )
            connection.commit()
            bot.send_message(
                call.message.chat.id,
                f'Данные успешно внесены! Корпус сменен на <code>{"".join([el for el in db.execute("SELECT korp FROM dop_ed WHERE id = ?", (time_help[2],)).fetchall()[0][0]])}</code>',
                parse_mode="HTML",
                reply_markup=bttns,
            )
        elif "no" in call.data:
            bot.send_message(
                call.message.chat.id, "Изменения не применены!", reply_markup=bttns
            )
        else:
            bot.send_message(
                call.message.chat.id,
                f'Данный кружок проводится: <code>{"".join([el for el in db.execute("SELECT korp FROM dop_ed WHERE id=?", (time_help[2],)).fetchall()[0][0]])}</code>\nНовый корпус введите ниже. <b>ВАЖНО!</b>\nКорпус выберите из предложенных ниже вариантов. Скопировать текст можно просто нажав на него:)\n1. <code>на Ломоносовском</code>\n2. <code>на Профсоюзной</code>\n3. <code>на Крижановского</code>',
                parse_mode="HTML",
            )
            bot.register_next_step_handler(
                call.message, change_data, "корпус", "korp", message_text
            )
    elif "type" in call.data:
        if "yes" in call.data:
            db.execute(
                """UPDATE dop_ed SET type = ? WHERE id = ?""",
                (message_text, time_help[2]),
            )
            connection.commit()
            bot.send_message(
                call.message.chat.id,
                f'Данные успешно внесены! Категория сменена на {"".join([el for el in db.execute("SELECT type FROM dop_ed WHERE id = ?", (time_help[2],)).fetchall()[0][0]])}',
                reply_markup=bttns,
            )
        elif "no" in call.data:
            bot.send_message(
                call.message.chat.id, "Изменения не применены!", reply_markup=bttns
            )
        else:
            bot.send_message(
                call.message.chat.id,
                f'Категория данного крука: <code>{"".join([el for el in db.execute("SELECT type FROM dop_ed WHERE id=?", (time_help[2],)).fetchall()[0][0]])}</code>\nНовую категорию введите ниже. <b>ВАЖНО!</b>\nКорпус выберите из предложенных ниже вариантов. Скопировать текст можно просто нажав на него:)\n1. <code>Физкультурно-спотривное</code>\n2. <code>Социально-педагогическое</code>\n3. <code>на Естественнонаучное</code>\n4. <code>Техническое</code>\n5. <code>Художественное</code>',
                parse_mode="HTML",
            )
            bot.register_next_step_handler(
                call.message, change_data, "тип кружка", "type", message_text
            )
    elif "push" or "take" in call.data:
        if "push" in call.data:
            bttns = types.InlineKeyboardMarkup(row_width=2)
            btn1 = types.InlineKeyboardButton("К списку админа", callback_data="admin")
            btn2 = types.InlineKeyboardButton(
                "К списку Кружков", callback_data="all_positions, page_1, remember"
            )
            btn3 = types.InlineKeyboardButton(
                "К кружку",
                callback_data=f"{int(time_help[2]) - 10000} position_details",
            )
            bttns.add(btn1, btn2, btn3)
            db.execute(
                "UPDATE dop_ed SET id=id-10000 WHERE id = ?",
                (call.data.split(", ")[2],),
            )
            bot.send_message(
                call.message.chat.id,
                "Данная запись теперь видна пользователям!",
                reply_markup=bttns,
            )
        else:
            bttns = types.InlineKeyboardMarkup(row_width=2)
            btn1 = types.InlineKeyboardButton("К списку админа", callback_data="admin")
            btn2 = types.InlineKeyboardButton(
                "К списку Кружков", callback_data="all_positions, page_1, remember"
            )
            btn3 = types.InlineKeyboardButton(
                "К кружку",
                callback_data=f"{int(time_help[2]) + 10000} position_details",
            )
            bttns.add(btn1, btn2, btn3)
            db.execute(
                "UPDATE dop_ed SET id=id+10000 WHERE id = ?",
                (call.data.split(", ")[2],),
            )
            bot.send_message(
                call.message.chat.id,
                "Данная запись теперь невидна пользователям!",
                reply_markup=bttns,
            )
        connection.commit()


def change_password_handler(call, bot):
    print("pass")


def add_handler(call, bot):
    print("add")


def logout_handler(call, bot):
    print("logout")


def create_data_handler(call, bot, db, connection):
    numbers = [int(el[0]) for el in db.execute("SELECT id FROM dop_ed").fetchall()]
    for i in range(1, max(numbers) + 1):
        if i not in numbers:
            new_id = i
            break
    else:
        new_id = max(numbers) + 1  # id, name, klasses, type, code, teacher, time, aud, plat, reg, sinse, korp
    db.execute("""INSERT INTO dop_ed (id, name, klasses, type, code, teacher, time, aud, plat, reg,
                    sinse, korp) VALUES (?, '❗Новая запись', '0', '*', '*', '*', '*:*-*:* *', '*', '-', '-', '-', ?)""",
               [int(new_id) + 10000, call.data.split(", ")[1]])
    btn = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton('К кружку',
                                   callback_data=f'{new_id + 10000} position_details'))  # Change call.data!!!
    bot.send_message(call.message.chat.id, 'Запись успешно создана!', reply_markup=btn)
    connection.commit()
