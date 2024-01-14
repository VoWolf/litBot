import telebot, sqlite3
from telebot import types

bot = telebot.TeleBot("6438520666:AAFmH9T9S8B3XmpEyQ4UXZWDWF4DBliDfL4")

admin = False
time_help = None
page_message_data = 0


@bot.message_handler(commands=['admin', 'login', 'reg'])
def check(message):
    bot.send_message(message.chat.id, 'Введите пароль: ')
    bot.register_next_step_handler(message, code_check)


@bot.message_handler(commands=['start'])
def start(message):
    bttns = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('Дополнительное образование', callback_data='main_1')
    btn2 = types.InlineKeyboardButton('Контактные данные', callback_data='main_2')
    btn3 = types.InlineKeyboardButton('Помощь', callback_data='help')
    bttns.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id,
                     'Здравствуйте! Я бот Лицея №1533 и могу ответить на ваши вопросы. Вот разделы которые в меня загружены:',
                     reply_markup=bttns)


@bot.message_handler(commands=['help'])
def help_message(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item = types.InlineKeyboardButton('Контактные данные', callback_data='main_question_2')
    item2 = types.InlineKeyboardButton('Главное меню', callback_data='restart')
    item3 = types.InlineKeyboardButton('Как записаться на доп. образование', callback_data='how_to_register?')
    markup.add(item, item2, item3)
    bot.send_message(message.chat.id, 'Данный бот предназначен для предоставления информации о дополнительном образовании. Если вы не нашли здесь нужной вам информации, обратитесь к администрации лицея (контактные данные откроются при нажатии на кнопку ниже) \n \n Воспользуйтесь командой /start или кнопкой под сообщением для возвпащения к главным опциям.', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect("data")
    c = conn.cursor()
    global page_message_data
    global  time_help
    if call.data == 'main_2':
        markup = types.InlineKeyboardMarkup(row_width=1)
        item = types.InlineKeyboardButton('Корпуса на карте',
                                          url='https://yandex.ru/maps/213/moscow/?ll=37.555258%2C55.691771&mode=usermaps&um=constructor%3A1nzJdcg6iOPjfPFPXyh90u3R46dsk_8W&z=15')
        item2 = types.InlineKeyboardButton('Номера телефонов и официальный сайт', callback_data='kontact_question_1')
        item3 = types.InlineKeyboardButton('Главная страница', callback_data='restart')
        item4 = types.InlineKeyboardButton('Как записаться на доп образование?', callback_data='how_to_register?')

        markup.add(item, item2, item3, item4)
        bot.send_message(call.message.chat.id, 'Доступная об администрации Лицея №1533:', reply_markup=markup)

    elif call.data == 'main_3':
        bttns = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton('Изменить список/структуру кружков', callback_data='Watch_all, page 1')
        btn2 = types.InlineKeyboardButton('Изменить пароль администратора', callback_data='Change_password')
        btn3 = types.InlineKeyboardButton('Выйти из аккаунта', callback_data='Logout')
        bttns.add(btn1, btn2, btn3)
        bot.send_message(call.message.chat.id, 'Вы на главной странице администратора!', reply_markup=bttns)

    elif call.data == 'kontact_question_1':
        markup = types.InlineKeyboardMarkup(row_width=1)  # сколько кнопок в ряд
        item = types.InlineKeyboardButton('Официальный сайт школы № 1533 «ЛИТ»', url='https://lyc1533.mskobr.ru/')
        item2 = types.InlineKeyboardButton('Расписание каникул', callback_data='holidays')
        item3 = types.InlineKeyboardButton('Главная страница', callback_data='restart')
        markup.add(item, item2, item3)
        bot.send_message(call.message.chat.id,
                         'Звоните с 9 до 18 часов в учебное время, а также с 10 до 16 во время каникул: \n +7 499 133-24-35 ... Ломоносовский, \n +7 499 124-55-65 ... Профсоюзная, \n +7 499 125-23-59 ... Кржижановского',
                         reply_markup=markup)

    elif call.data == 'help':
        markup = types.InlineKeyboardMarkup(row_width=1)
        item = types.InlineKeyboardButton('Контактные данные', callback_data='main_question_2')
        item2 = types.InlineKeyboardButton('Главная страница', callback_data='restart')
        item3 = types.InlineKeyboardButton('Как записаться на доп. образование', callback_data='how_to_register?')
        markup.add(item, item2, item3)
        bot.send_message(call.message.chat.id,
                         'Данный бот предназначен для предоставления информации о дополнительном образовании. Если вы не нашли здесь нужной вам информации, обратитесь к администрации лицея (контактные данные откроются при нажатии на кнопку ниже) \n\n Воспользуйтесь командой /start или кнопкой под сообщением для возвращения в главное меню.',
                         reply_markup=markup)

    elif call.data == 'restart':
        bttns = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton('Дополнительное образование', callback_data='main_1')
        btn2 = types.InlineKeyboardButton('Контактные данные', callback_data='main_2')
        btn3 = types.InlineKeyboardButton('Помощь', callback_data='help')
        bttns.add(btn1, btn2, btn3)
        bot.send_message(call.message.chat.id,
                         'Здравствуйте! Я бот Лицея №1533 и могу ответить на ваши вопросы. Вот разделы которые в меня загружены:',
                         reply_markup=bttns)

    elif call.data == 'holidays':
        f = open('./holidays_2023-2024.png', 'rb')
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('Главная страница', callback_data='restart')
        btn2 = types.InlineKeyboardButton('К номерам телефона', callback_data='kontact_question_1')
        markup.add(btn1, btn2)
        bot.send_photo(call.message.chat.id, f, 'Расписание каникул 2023-2024!', reply_markup=markup)

    elif call.data == 'how_to_register?':
        bttns = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton('Обратно', callback_data='main_2')
        btn2 = types.InlineKeyboardButton('К выбору кружка', callback_data='main_1')
        bttns.add(btn, btn2)
        bot.send_message(call.message.chat.id,
                         'Это делается через сайт mos.ru. Вот подробная инструкция по записи:\n1.Зайдите на сайт mos.ru и войдите в аккаунт\n2. Сверху перечислены разделы, перейдите в раздул "услуги"\n3. В меню слева выбираете услугу "образование". Если ее не видно, воспользуйтесь строкой для поиска.\n4.Когда вы выберите услугу "образование" чуть правее появиться выбор раздела. Выберите "допобразование"\n4. Еще правее выберите пункт "Запись в кружки, спортивные секции, дома творчества", нажмите на него.\n5. Подтвердите свой выбор нажав на кнопку "Получить услугу"\n6. В открывшемся окне выберите пункт "запись в кружок", ниже введите код кружка (его моно получить в этом боте)\n7. Дальше следуйте инструкциям на сайте, удачи!',
                         reply_markup=bttns)

    elif call.data == 'main_1':
        bttns = types.InlineKeyboardMarkup()
        bttns.row(types.InlineKeyboardButton('На Профсоюзной', callback_data='Profsousnyaa'))
        bttns.row(types.InlineKeyboardButton('На Ломоносовском', callback_data='Lomonosovsky'))
        bttns.row(types.InlineKeyboardButton('На Крижановского', callback_data='Krizhanovskogo'))
        bttns.row(types.InlineKeyboardButton('Все наши кружки', callback_data='all_positions, page_1, remember'))
        bttns.row(types.InlineKeyboardButton('Главная', callback_data='restart'),
                  types.InlineKeyboardButton('Помощь', callback_data='help'))

        bot.send_message(call.message.chat.id, 'Кружки в каком корпусе вас интересуют?', reply_markup=bttns)

    elif call.data == 'Profsousnyaa':
        positions = c.execute("SELECT * FROM dop_ed WHERE korp = 'на Профсоюзной'").fetchall()
        bttns = types.InlineKeyboardMarkup()
        if admin:
            bttns.row(types.InlineKeyboardButton('Добавить запись', callback_data='Add_data, на Профсоюзной'))
        bttns.row(types.InlineKeyboardButton('Главная', callback_data='restart'),
                  types.InlineKeyboardButton('Помощь', callback_data='help'))
        if positions == []:
            bot.send_message(call.message.chat.id, 'К сожалению, кружков на Профсоюзной не добавлено!',
                             reply_markup=bttns)
        else:
            for el in positions:
                if el[0] < 10000 or admin:
                    if len(str(el[2]).split()) > 1:
                        bttns.add(types.InlineKeyboardButton(
                            f'{el[1]} для {', '.join(str(el[2]).split()[0:-1])} и {str(el[2]).split()[-1]} классов',
                            callback_data=f'{el[0]} look_at_position'))
                    else:
                        bttns.add(types.InlineKeyboardButton(f'{el[1]} для {str(el[2]).split()[-1]} классов',
                                                             callback_data=f'{el[0]} look_at_position'))
            bot.send_message(call.message.chat.id, 'Кружки на Профсоюзной:', reply_markup=bttns)

    elif call.data == 'Lomonosovsky':
        positions = c.execute("SELECT * FROM dop_ed WHERE korp = 'на Ломоносовском'").fetchall()
        print(positions)
        bttns = types.InlineKeyboardMarkup()
        if admin:
            bttns.row(types.InlineKeyboardButton('Добавить запись', callback_data='Add_data, на Профсоюзной'))
        bttns.row(types.InlineKeyboardButton('Главная', callback_data='restart'),
                  types.InlineKeyboardButton('Помощь', callback_data='help'))
        if positions == []:
            bot.send_message(call.message.chat.id, 'К сожалению, кружков на Ломоносовском не добавлено!',
                             reply_markup=bttns)
        else:
            for el in positions:
                if el[0] < 10000 or admin:
                    if len(str(el[2]).split()) > 1:
                        bttns.add(types.InlineKeyboardButton(
                            f'{el[1]} для {', '.join(str(el[2]).split()[0:-1])} и {str(el[2]).split()[-1]} классов',
                            callback_data=f'{el[0]} look_at_position'))
                    else:
                        bttns.add(types.InlineKeyboardButton(f'{el[1]} для {str(el[2]).split()[-1]} классов',
                                                             callback_data=f'{el[0]} look_at_position'))
            bot.send_message(call.message.chat.id, 'Кружки на Ломоносовском:', reply_markup=bttns)

    elif call.data == 'Krizhanovskogo':
        positions = c.execute("SELECT * FROM dop_ed WHERE korp = 'на Крижановского'").fetchall()
        bttns = types.InlineKeyboardMarkup()
        if admin:
            bttns.row(types.InlineKeyboardButton('Добавить запись', callback_data='Add_data, на Профсоюзной'))
        bttns.row(types.InlineKeyboardButton('Главная', callback_data='restart'),
                  types.InlineKeyboardButton('Помощь', callback_data='help'))
        if positions == []:
            bot.send_message(call.message.chat.id, 'К сожалению, кружков на Крижановского не добавлено!',
                             reply_markup=bttns)
        else:
            for el in positions:
                if el[0] < 10000 or admin:
                    if len(str(el[2]).split()) > 1:
                        bttns.add(types.InlineKeyboardButton(
                            f'{el[1]} для {', '.join(str(el[2]).split()[0:-1])} и {str(el[2]).split()[-1]} классов',
                            callback_data=f'{el[0]} look_at_position'))
                    else:
                        bttns.add(types.InlineKeyboardButton(f'{el[1]} для {str(el[2]).split()[-1]} классов',
                                                             callback_data=f'{el[0]} look_at_position'))
            bot.send_message(call.message.chat.id, 'Кружки на Крижановского:', reply_markup=bttns)

    elif 'all_positions' in call.data:
        if 'page_1' in call.data:
            if 'remember' in call.data:
                page_message_data = call.message.id + 1
            bttns = types.InlineKeyboardMarkup()
            data: list = c.execute(
                """SELECT id, name, klasses FROM dop_ed WHERE korp = 'на Ломоносовском'""").fetchall()
            btn1 = types.InlineKeyboardButton('На стр. 2', callback_data='all_positions, page_2')
            bttns.row(btn1)
            if data == []:
                if admin:
                    bttns.row(
                        types.InlineKeyboardButton('Создать запись', callback_data='Create_data, на Ломоносовском'))
                    if 'remember' in call.data:
                        bot.send_message(call.message.chat.id,
                                         'Стр 1/3: Ломносовский\nПредыдущая: функции\nСледующая: Профсоюзная\nКружков на Ломоносовском пока что не добавлено!',
                                         reply_markup=bttns)
                    else:
                        bot.edit_message_text(
                            'Стр 1/3: Ломносовский\nПредыдущая: функции\nСледующая: Профсоюзная\nКружков на Ломоносовском пока что не добавлено!',
                            call.message.chat.id, page_message_data, reply_markup=bttns)
                else:
                    if 'remember' in call.data:
                        bot.send_message(call.message.chat.id,
                                         'Стр 1/3: Ломносовский\nСледующая: Профсоюзная\nКружков на Ломоносовском пока что не добавлено, пожалуйста, обратитесь в администрациию для записи!',
                                         reply_markup=bttns)
                    else:
                        bot.edit_message_text(
                            'Стр 1/3: Ломносовский\nСледующая: Профсоюзная\nКружков на Ломоносовском пока что не добавлено, пожалуйста, обратитесь в администрациию для записи!',
                            call.message.chat.id, page_message_data, reply_markup=bttns)
            else:
                for el in data:
                    if el[0] < 10000 or admin:
                        if len(str(el[2]).split()) > 1:
                            bttns.add(types.InlineKeyboardButton(
                                f'{el[1]} для {', '.join(str(el[2]).split()[0:-1])} и {str(el[2]).split()[-1]} классов',
                                callback_data=f"{el[0]} look_at_position"))
                        else:
                            bttns.add(types.InlineKeyboardButton(f'{el[1]} для {str(el[2]).split()[-1]} классов',
                                                                 callback_data=f"{el[0]} look_at_position"))
                if admin:
                    if 'remember' not in call.data:
                        bot.edit_message_text(
                            'Стр 1/3: Ломносовский\nСледующая: Профсоюзная\nСписок доступных к изменению кружков:',
                            call.message.chat.id, page_message_data, reply_markup=bttns)
                    else:
                        bot.send_message(call.message.chat.id,
                                         'Стр 1/3: Ломносовский\nСледующая: Профсоюзная\nСписок доступных к изменению кружков:',
                                         reply_markup=bttns)
                else:
                    if 'remember' not in call.data:
                        bot.edit_message_text(
                            'Стр 1/3: Ломносовский\nСледующая: Профсоюзная\nСписок доступных кружков:',
                            call.message.chat.id, page_message_data, reply_markup=bttns)
                    else:
                        bot.send_message(call.message.chat.id,
                                         'Стр 1/3: Ломносовский\nСледующая: Профсоюзная\nСписок доступных кружков:',
                                         reply_markup=bttns)
        elif 'page_2' in call.data:
            bttns = types.InlineKeyboardMarkup()
            data: list = c.execute("""SELECT id, name, klasses FROM dop_ed WHERE korp = 'на Профсоюзной'""").fetchall()
            btn1 = types.InlineKeyboardButton('На стр. 1', callback_data='all_positions, page_1')
            btn2 = types.InlineKeyboardButton('На стр. 3', callback_data='all_positions, page_3')
            bttns.row(btn1, btn2)
            if data == []:
                if admin:
                    bttns.row(types.InlineKeyboardButton('Создать запись', callback_data='Create_data, на Профсоюзной'))
                    bot.edit_message_text(
                        'Стр 2/3: Профсоюзная\nПредыдущая: Ломоносовский\nСледующая: Крижановского\nКружков на Профсоюзной пока что не добавлено!',
                        call.message.chat.id, page_message_data, reply_markup=bttns)
                else:
                    bot.edit_message_text(
                        'Стр 2/3: Профсоюзная\nПредыдущая: Ломоносовский\nСледующая: Крижановского\nКружков на Профсоюзной пока что не добавлено, пожалуйста, обратитесь в администрациию для записи!',
                        call.message.chat.id, page_message_data, reply_markup=bttns)
            else:
                for el in data:
                    if el[0] < 10000 or admin:
                        if len(str(el[2]).split()) > 1:
                            bttns.add(types.InlineKeyboardButton(
                                f'{el[1]} для {', '.join(str(el[2]).split()[0:-1])} и {str(el[2]).split()[-1]} классов',
                                callback_data=f"{el[0]} look_at_position"))
                        else:
                            bttns.add(types.InlineKeyboardButton(f'{el[1]} для {str(el[2]).split()[-1]} классов',
                                                                 callback_data=f"{el[0]} look_at_position"))
                if admin:
                    bot.edit_message_text(
                        'Стр 2/3: Профсоюзная\nПредыдущая: Ломоносовский\nСледующая: Крижановского\nСписок доступных к изменению кружков:',
                        call.message.chat.id, page_message_data, reply_markup=bttns)
                else:
                    bot.edit_message_text(
                        'Стр 2/3: Профсоюзная\nПредыдущая: Ломоносовский\nСледующая: Крижановского\nСписок доступных кружков:',
                        call.message.chat.id, page_message_data, reply_markup=bttns)
        elif 'page_3' in call.data:
            bttns = types.InlineKeyboardMarkup()
            data: list = c.execute(
                """SELECT id, name, klasses FROM dop_ed WHERE korp = 'на Крижановского'""").fetchall()
            btn1 = types.InlineKeyboardButton('На стр. 2', callback_data='all_positions, page_2')
            bttns.row(btn1)
            if data == []:
                if admin:
                    bttns.row(
                        types.InlineKeyboardButton('Создать запись', callback_data='Create_data, на Крижановского'))
                    bot.edit_message_text(
                        'Стр 3/3: Крижановского:\nПредыдущая: Профсоюзная\nКружков на Крижановского не добавлено!',
                        call.message.chat.id, page_message_data, reply_markup=bttns)
                else:
                    bot.edit_message_text(
                        'Стр 3/3: Крижановского:\nПредыдущая: Профсоюзная\nКружков на Крижановского пока что не добавлено, пожалуйста, обратитесь в администрациию для записи!',
                        call.message.chat.id, page_message_data, reply_markup=bttns)
            else:
                for el in data:
                    if el[0] < 10000 or admin:
                        if len(str(el[2]).split()) > 1:
                            bttns.add(types.InlineKeyboardButton(
                                f'{el[1]} для {', '.join(str(el[2]).split()[0:-1])} и {str(el[2]).split()[-1]} классов',
                                callback_data=f"{el[0]} look_at_position"))
                        else:
                            bttns.add(types.InlineKeyboardButton(f'{el[1]} для {str(el[2]).split()[-1]} классов',
                                                                 callback_data=f"{el[0]} look_at_position"))
                if admin:
                    bot.edit_message_text(
                        'Стр 3/3: Крижановского:\nПредыдущая: Профсоюзная\nСписок доступных к изменению кружков:',
                        call.message.chat.id, page_message_data, reply_markup=bttns)
                else:
                    bot.edit_message_text('Стр 3/3: Крижановского:\nПредыдущая: Профсоюзная\nСписок доступных кружков:',
                                          call.message.chat.id, page_message_data, reply_markup=bttns)

    elif 'look_at_position' in call.data:
        bttns = types.InlineKeyboardMarkup(row_width=2)
        btn0 = types.InlineKeyboardButton('К кружкам', callback_data='all_positions, page_1, remember')
        btn1 = types.InlineKeyboardButton('Главная', callback_data='restart')
        bttns.row(btn0, btn1)
        result = c.execute("""SELECT * FROM dop_ed WHERE id = ?""", (call.data.split()[0],)).fetchone()
        if admin:
            btn1 = types.InlineKeyboardButton('Название', callback_data=f'Change_data, name, {result[0]}')
            btn2 = types.InlineKeyboardButton('Доступные классы', callback_data=f'Change_data, klass, {result[0]}')
            btn3 = types.InlineKeyboardButton('Имя преподавателя',
                                              callback_data=f'Change_data, teacher_name, {result[0]}')
            btn4 = types.InlineKeyboardButton('Время проведения', callback_data=f'Change_data, time, {result[0]}')
            btn5 = types.InlineKeyboardButton('Аудиторию', callback_data=f'Change_data, aud, {result[0]}')
            if result[-4] == '-':
                btn6 = types.InlineKeyboardButton('Сделать платным',
                                                  callback_data=f'Change_data, do_plat_yes, {result[0]}')
            else:
                btn6 = types.InlineKeyboardButton('Сделать бесплатным',
                                                  callback_data=f'Change_data, do_plat_no, {result[0]}')
            btn7 = types.InlineKeyboardButton('Дату старта', callback_data=f'Change_data, start_date, {result[0]}')
            if result[9] == '+':
                btn8 = types.InlineKeyboardButton('Код для записи', callback_data=f'Change_data, kode, {result[0]}')
                bttns.add(btn8)
                btn9 = types.InlineKeyboardButton('Скрыть код', callback_data=f'Change_data, remove_kode, {result[0]}')
            else:
                btn9 = types.InlineKeyboardButton('Показать код', callback_data=f'Change_data, show_kode, {result[0]}')
            btn10 = types.InlineKeyboardButton('Изменить тип', callback_data=f'Change_data, type, {result[0]}')
            btn11 = types.InlineKeyboardButton('Удалить запись', callback_data=f'Change_data, remove, {result[0]}')
            btn12 = types.InlineKeyboardButton('Корпус', callback_data=f'Change_data, korp, {result[0]}')
            btn13 = types.InlineKeyboardButton('Категорию', callback_data=f'Change_data, type, {result[0]}, 0')
            bttns.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn9, btn10, btn11, btn12, btn13)
            if result[0] > 10000:
                bttns.add(types.InlineKeyboardButton('PUSH', callback_data=f'Change_data, push, {result[0]}'))
            else:
                bttns.add(types.InlineKeyboardButton('TAKE', callback_data=f'Change_data, take, {result[0]}'))

        ans = ''

        help = str(result[2]).split()
        if len(help) > 1:
            ans += f'{result[1]} для {', '.join(str(result[2]).split()[0:-1]) + ' и ' + str(result[2]).split()[-1]} классов на {result[-1]}:\n\n'
        else:
            ans += f'{result[1]} для {', '.join(str(result[2]).split())} классов:\n'
        ans += f'Преподаватель: {result[5]}\n'
        time = result[6].split()
        if '$' not in time:
            startend = time[0].split('-')
            start = startend[0]
            end = startend[1]
            ans += f'Проходит с {start} до {end}, по {time[1]}\n'
        else:
            del time[0]
            ans += f'Имеется 2 группы: \n1 группа: с {time[0].split("-")[0]} до {time[0].split("-")[1]}\n2 группа: с {time[1].split("-")[0]} до {time[1].split("-")[1]}\nПо {time[2]}\n'
        ans += f'Аудитория: {result[7]}\n'
        if result[-4] == '+':
            ans += 'Данный кружок является платным!\n'
        if result[-2] != '-':
            ans += f'Данный кружок начинается {result[-2]}'
        if result[9] == '+':
            ans += f'\nКод для записи на mos.ru: <code>{result[4]}</code> (нажмите чтобы скопировать)'
        else:
            ans += 'Данный кружок не требует записи на mos.ru'
        if admin:
            bot.send_message(call.message.chat.id, f"{ans}\n\nЧто хотите изменить?", parse_mode='HTML',
                             reply_markup=bttns)
        else:
            bot.send_message(call.message.chat.id, ans, parse_mode='HTML', reply_markup=bttns)

    elif 'Change_data' in call.data:
        conn = sqlite3.connect("data")
        c = conn.cursor()

        time_help = call.data.split(", ")
        bttns = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('К списку админа', callback_data='main_3')
        btn2 = types.InlineKeyboardButton('К списку Кружков', callback_data='all_positions, page_1, remember')
        btn3 = types.InlineKeyboardButton('К кружку', callback_data=f'{time_help[2]} look_at_position')
        bttns.add(btn1, btn2, btn3)

        if 'teacher_name' in call.data:
            if 'yes' in call.data:
                c.execute("""UPDATE dop_ed SET teacher = ? WHERE id = ?""",
                            (do_not_touch_or_this_bot_will_crash, time_help[2]))
                conn.commit()
                bot.send_message(call.message.chat.id,
                                 f'Данные успешно внесены! Новое имя пеподавателя: <code>{"".join([el for el in c.execute("SELECT teacher FROM dop_ed WHERE id = ?", (time_help[2],)).fetchone()[0]])}</code>',
                                 reply_markup=bttns, parse_mode='HTML')
            elif 'no' in call.data:
                bot.send_message(call.message.chat.id, 'Изменения не применены!', reply_markup=bttns)
            else:
                bot.send_message(call.message.chat.id,
                                 f"Текущее имя учителя: <code>{' '.join([el[0] for el in c.execute("SELECT teacher FROM dop_ed WHERE id=?", (time_help[2],))])}</code>\nНовое имя ниже",
                                 parse_mode='HTML')
                bot.register_next_step_handler(call.message, change_data, 'имя учителя', 'teacher_name')
        elif 'name' in call.data:
            if 'yes' in call.data:
                c.execute("""UPDATE dop_ed SET name = ? WHERE id = ?""",
                            (do_not_touch_or_this_bot_will_crash, time_help[2]))
                conn.commit()
                bot.send_message(call.message.chat.id,
                                 f'Данные успешно внесены! Новое название: <code>{"".join([el for el in c.execute("SELECT name FROM dop_ed WHERE id = ?", (time_help[2],)).fetchone()[0]])}</code>',
                                 reply_markup=bttns, parse_mode='HTML')
            elif 'no' in call.data:
                bot.send_message(call.message.chat.id, 'Изменения не применены!', reply_markup=bttns)
            else:
                bot.send_message(call.message.chat.id,
                                 f" Текущее имя: <code>{' '.join([el[0] for el in c.execute("SELECT name FROM dop_ed WHERE id=?", (time_help[2],))])}</code>\nНовое имя введите ниже",
                                 parse_mode='HTML')
                bot.register_next_step_handler(call.message, change_data, 'имя', 'name')
        elif 'klass' in call.data:
            if 'yes' in call.data:
                c.execute("""UPDATE dop_ed SET klasses = ? WHERE id = ?""",
                          (do_not_touch_or_this_bot_will_crash, time_help[2]))
                conn.commit()
                bot.send_message(call.message.chat.id,
                                 f'Данные успешно внесены! Классы, которым можно посещаять занятия: <code>{", ".join([str(el) for el in c.execute("SELECT klasses FROM dop_ed WHERE id = ?", (time_help[2],)).fetchone()[0]])}</code>',
                                 reply_markup=bttns, parse_mode='HTML')
            elif 'no' in call.data:
                bot.send_message(call.message.chat.id, 'Изменения не применены!', reply_markup=bttns)
            else:
                bot.send_message(call.message.chat.id,
                                 f" Текущее значение допускаемых классов: <code>{' '.join([str(el[0]) for el in c.execute("SELECT klasses FROM dop_ed WHERE id=?", (time_help[2],))])}</code>\nНовое значение введите ниже",
                                 parse_mode='HTML')
                bot.register_next_step_handler(call.message, change_data, 'значения', 'klass')
        elif 'time' in call.data:
            if 'yes' in call.data:
                c.execute("""UPDATE dop_ed SET time = ? WHERE id = ?""",
                          (do_not_touch_or_this_bot_will_crash, time_help[2]))
                conn.commit()
                bot.send_message(call.message.chat.id, 'Данные успешно внесены!', reply_markup=bttns)
            elif 'no' in call.data:
                bot.send_message(call.message.chat.id, 'Изменения не применены!', reply_markup=bttns)
            else:
                time = c.execute("""SELECT time FROM dop_ed WHERE id = ?""", (time_help[2],)).fetchall()[0][0]
                time = time.split()
                if '$' not in time:
                    start = time[0].split('-')[0]
                    end = time[0].split('-')[1]
                    bot.send_message(call.message.chat.id,
                                     f" Текущее время проведения: \nВремя начала: <code>{start}</code> \nВремя окончания: <code>{end}</code> \nДень недели (проведения): <code>{time[1]}</code> \nНовое значение введите ниже в формате ([время начала]-[время окончания] [день недели в дательном падеже]). Если хотите изменить время проведения по группам (Группа 1, группа 2), то воспользуйтесь другим форматом: ($ [Время начала занятий 1-й группы]-[Время окончания занятий 1-й группы] [Время начала занятий 2-й группы]-[Время окончания занятий 2-й группы] [День недели в дательном падеже]):",
                                     parse_mode='HTML')
                else:
                    del time[0]
                    gr_1_start = time[0].split("-")[0]
                    gr_1_end = time[0].split("-")[1]
                    gr_2_start = time[1].split("-")[0]
                    gr_2_end = time[1].split("-")[1]
                    bot.send_message(call.message.chat.id,
                                     f'Текущее время проведения: \n1 группа: с {gr_1_start} до {gr_1_end}\n2 группа: с {gr_2_start} до {gr_2_end}\nПо {time[2]}. \nНовое значение введите ниже в формате ([время начала]-[время окончания] [день недели в дательном падеже]). Если хотите изменить время проведения по группам (Группа 1, группа 2), то воспользуйтесь другим форматом: ($ [Время начала занятий 1-й группы]-[Время окончания занятий 1-й группы] [Время начала занятий 2-й группы]-[Время окончания занятий 2-й группы] [День недели в дательном падеже]):',
                                     parse_mode='HTML')

                bot.register_next_step_handler(call.message, change_data, 'время проведения', 'time')
        elif 'aud' in call.data:
            if 'yes' in call.data:
                c.execute("""UPDATE dop_ed SET aud = ? WHERE id = ?""",
                          (do_not_touch_or_this_bot_will_crash, time_help[2]))
                conn.commit()
                bot.send_message(call.message.chat.id,
                                 f'Данные успешно внесены! Аудитория изменена на <code>{"".join([el for el in c.execute("SELECT aud FROM dop_ed WHERE id = ?", (time_help[2],)).fetchone()[0]])}</code>',
                                 reply_markup=bttns, parse_mode='HTML')
            elif 'no' in call.data:
                bot.send_message(call.message.chat.id, 'Изменения не применены!', reply_markup=bttns)
            else:
                bot.send_message(call.message.chat.id,
                                 f" Текущее место проведения: <code>{' '.join([el[0] for el in c.execute("SELECT aud FROM dop_ed WHERE id=?", (time_help[2],))])}</code>\nНовое место проведения занятий введите ниже",
                                 parse_mode='HTML')
                bot.register_next_step_handler(call.message, change_data, 'место проведения занятий', 'aud')
        elif 'do_plat_yes' in call.data or 'do_plat_no' in call.data:
            if 'do_plat_yes' in call.data:
                c.execute("""UPDATE dop_ed SET plat = ? WHERE id = ?""", ('+', time_help[2]))
                bot.send_message(call.message.chat.id, 'Кружок сделан платным!', reply_markup=bttns)
            else:
                c.execute("""UPDATE dop_ed SET plat = ? WHERE id = ?""", ('-', time_help[2]))
                bot.send_message(call.message.chat.id, 'Кружок сделан бесплатным!', reply_markup=bttns)
            conn.commit()
        elif 'start_date' in call.data:
            if 'yes' in call.data:
                c.execute("""UPDATE dop_ed SET sinse = ? WHERE id = ?""",
                          (do_not_touch_or_this_bot_will_crash, time_help[2]))
                conn.commit()
                bot.send_message(call.message.chat.id,
                                 f'Данные успешно внесены! Время старта занятий изменено на <code>{"".join([el for el in c.execute("SELECT sinse FROM dop_ed WHERE id = ?", (time_help[2],)).fetchone()[0]])}</code>',
                                 reply_markup=bttns, parse_mode='HTML')
            elif 'no' in call.data:
                bot.send_message(call.message.chat.id, 'Изменения не применены!', reply_markup=bttns)
            else:
                if ' '.join(
                        [el[0] for el in c.execute("SELECT sinse FROM dop_ed WHERE id=?", (time_help[2],))]) == '-':
                    bot.send_message(call.message.chat.id,
                                     'Дата старта данного кружка не указана (=> стартует 1 сент.), новое значение укажите ниже:')
                else:
                    bot.send_message(call.message.chat.id,
                                     f"Текущая дата старта: <code>{' '.join([el[0] for el in c.execute("SELECT sinse FROM dop_ed WHERE id=?", (time_help[2],))])}</code>\nНовую дату старта укажите ниже (напишите '<code>-</code>' если дата старта 1 сентября):",
                                     parse_mode='HTML')
                bot.register_next_step_handler(call.message, change_data, 'дата старта', 'start_date')
                bot.register_next_step_handler(call.message, change_data, 'значения', 'klass')
        elif 'remove_kode' in call.data or 'show_kode' in call.data:
            if 'remove_kode' in call.data:
                if 'yes' in call.data:
                    c.execute("""UPDATE dop_ed SET reg = '-', code = '-' WHERE id = ?""", (time_help[2],))
                    conn.commit()
                    bot.send_message(call.message.chat.id, 'Регистрация на данный кружок отменена!',
                                     reply_markup=bttns)
                elif 'no' in call.data:
                    bot.send_message(call.message.chat.id, 'Действия не применены!', reply_markup=bttns)
                else:
                    cc = types.InlineKeyboardMarkup(row_width=1)
                    btn1 = types.InlineKeyboardButton('Подтвердить действия',
                                                      callback_data=f'Change_data, remove_kode, {time_help[2]}, yes')
                    btn2 = types.InlineKeyboardButton('Не подтверждать действия',
                                                      callback_data=f'Change_data, remove_kode, {time_help[2]}, no')
                    cc.add(btn1, btn2)
                    bot.send_message(call.message.chat.id,
                                     f'Вы уверены что хотите отменить регистрацию на кружок {"".join([str(el) for el in c.execute("SELECT name FROM dop_ed WHERE id = ?", (time_help[2],)).fetchall()[0]])}? <b>Внимание!</b> При подтверждении действия текущий код (<code>{''.join([str(el) for el in c.execute("SELECT code FROM dop_ed WHERE id = ?", (time_help[2],)).fetchall()[0]])}</code>) будет стерт!',
                                     parse_mode='HTML', reply_markup=cc)
            elif 'show_kode' in call.data:
                if 'yes' in call.data:
                    c.execute("""UPDATE dop_ed SET reg = '+', code = ? WHERE id = ?""",
                              (do_not_touch_or_this_bot_will_crash, time_help[2]))
                    conn.commit()
                    bot.send_message(call.message.chat.id,
                                     f'Регистрация на данный кружок введена. Новый код: <code>{do_not_touch_or_this_bot_will_crash}</code>',
                                     reply_markup=bttns, parse_mode='HTML')
                elif 'no' in call.data:
                    bot.send_message(call.message.chat.id, 'Действия не применены!', reply_markup=bttns)
                else:
                    bot.send_message(call.message.chat.id, f'Все почти готово! Ниже введите код кружка:')
                    bot.register_next_step_handler(call.message, change_data, 'код', 'show_kode')
        elif 'kode' in call.data:
            if 'yes' in call.data:
                c.execute("""UPDATE dop_ed SET code = ? WHERE id = ?""",
                          (do_not_touch_or_this_bot_will_crash, time_help[2]))
                conn.commit()
                bot.send_message(call.message.chat.id,
                                 f'Данные успешно внесены! Код сменен на <code>{"".join([str(el) for el in c.execute("SELECT code FROM dop_ed WHERE id = ?", (time_help[2],)).fetchone()[0]])}</code>',
                                 reply_markup=bttns, parse_mode='HTML')
            elif 'no' in call.data:
                bot.send_message(call.message.chat.id, 'Изменения не применены!', reply_markup=bttns)
            else:
                bot.send_message(call.message.chat.id,
                                 f"Текущий код для записи: <code>{' '.join([str(el[0]) for el in c.execute("SELECT code FROM dop_ed WHERE id=?", (time_help[2],))])}</code>\nНовый код введите ниже",
                                 parse_mode='HTML')
                bot.register_next_step_handler(call.message, change_data, 'код для записи', 'kode')
        elif 'remove' in call.data:
            if 'yes' in call.data:
                c.execute("""DELETE FROM dop_ed WHERE id = ?""", (time_help[2],))
                conn.commit()
                bot.send_message(call.message.chat.id, 'Запись удалена!',
                                 reply_markup=types.InlineKeyboardMarkup().add(
                                     types.InlineKeyboardButton('К куржкам',
                                                                callback_data='Watch_all, page_1, remember')))
            elif 'no' in call.data:
                bot.send_message(call.messae.chat.id, 'Запись не удалена!',
                                 reply_markup=types.InlineKeyboardMarkup().add(
                                     types.InlineKeyboardButton('К куржкам',
                                                                callback_data='Watch_all, page_1, remember')))
            else:
                cc = types.InlineKeyboardMarkup(row_width=1)
                btn1 = types.InlineKeyboardButton('Подтвердить действия',
                                                  callback_data=f'Change_data, remove, {time_help[2]}, yes')
                btn2 = types.InlineKeyboardButton('Не подтверждать действия',
                                                  callback_data=f'Change_data, remove, {time_help[2]}, no')
                cc.add(btn1, btn2)
                bot.send_message(call.message.chat.id,
                                 f'Вы уверены что хотите удалить запись о {"".join([str(el[0]) for el in c.execute("SELECT name FROM dop_ed WHERE id = ?", (time_help[2],)).fetchall()])}? <b>ОНА БУДЕТ БЕЗВОЗВРАТНО УТЕРЯНА</b>',
                                 parse_mode='HTML', reply_markup=cc)
        elif 'korp' in call.data:
            if 'yes' in call.data:
                c.execute("""UPDATE dop_ed SET korp = ? WHERE id = ?""",
                          (do_not_touch_or_this_bot_will_crash, time_help[2]))
                conn.commit()
                bot.send_message(call.message.chat.id,
                                 f'Данные успешно внесены! Корпус сменен на <code>{"".join([el for el in c.execute("SELECT korp FROM dop_ed WHERE id = ?", (time_help[2],)).fetchall()[0][0]])}</code>',
                                 parse_mode='HTML', reply_markup=bttns)
            elif 'no' in call.data:
                bot.send_message(call.message.chat.id, 'Изменения не применены!', reply_markup=bttns)
            else:
                bot.send_message(call.message.chat.id,
                                 f"Данный кружок проводится: <code>{''.join([el for el in c.execute("SELECT korp FROM dop_ed WHERE id=?", (time_help[2],)).fetchall()[0][0]])}</code>\nНовый корпус введите ниже. <b>ВАЖНО!</b>\nКорпус выберите из предложенных ниже вариантов. Скопировать текст можно просто нажав на него:)\n1. <code>на Ломоносовском</code>\n2. <code>на Профсоюзной</code>\n3. <code>на Крижановского</code>",
                                 parse_mode='HTML')
                bot.register_next_step_handler(call.message, change_data, 'корпус', 'korp')
        elif 'type' in call.data:
            if 'yes' in call.data:
                c.execute("""UPDATE dop_ed SET type = ? WHERE id = ?""",
                          (do_not_touch_or_this_bot_will_crash, time_help[2]))
                conn.commit()
                bot.send_message(call.message.chat.id,
                                 f'Данные успешно внесены! Категория сменена на {"".join([el for el in c.execute("SELECT type FROM dop_ed WHERE id = ?", (time_help[2],)).fetchall()[0][0]])}',
                                 reply_markup=bttns)
            elif 'no' in call.data:
                bot.send_message(call.message.chat.id, 'Изменения не применены!', reply_markup=bttns)
            else:
                bot.send_message(call.message.chat.id,
                                 f"Категория данного крука: <code>{''.join([el for el in c.execute("SELECT type FROM dop_ed WHERE id=?", (time_help[2],)).fetchall()[0][0]])}</code>\nНовую категорию введите ниже. <b>ВАЖНО!</b>\nКорпус выберите из предложенных ниже вариантов. Скопировать текст можно просто нажав на него:)\n1. <code>Физкультурно-спотривное</code>\n2. <code>Социально-педагогическое</code>\n3. <code>на Естественнонаучное</code>\n4. <code>Техническое</code>\n5. <code>Художественное</code>",
                                 parse_mode='HTML')
                bot.register_next_step_handler(call.message, change_data, 'тип кружка', 'type')
        elif 'push' or 'take' in call.data:
            if 'push' in call.data:
                bttns = types.InlineKeyboardMarkup(row_width=2)
                btn1 = types.InlineKeyboardButton('К списку админа', callback_data='main_3')
                btn2 = types.InlineKeyboardButton('К списку Кружков', callback_data='all_positions, page_1, remember')
                btn3 = types.InlineKeyboardButton('К кружку', callback_data=f'{int(time_help[2]) - 10000} look_at_position')
                bttns.add(btn1, btn2, btn3)
                c.execute("UPDATE dop_ed SET id=id-10000 WHERE id = ?", (call.data.split(", ")[2],))
                bot.send_message(call.message.chat.id, 'Данная запись теперь видна пользователям!', reply_markup=bttns)
            else:
                bttns = types.InlineKeyboardMarkup(row_width=2)
                btn1 = types.InlineKeyboardButton('К списку админа', callback_data='main_3')
                btn2 = types.InlineKeyboardButton('К списку Кружков', callback_data='all_positions, page_1, remember')
                btn3 = types.InlineKeyboardButton('К кружку', callback_data=f'{int(time_help[2]) + 10000} look_at_position')
                bttns.add(btn1, btn2, btn3)
                c.execute("UPDATE dop_ed SET id=id+10000 WHERE id = ?", (call.data.split(", ")[2],))
                bot.send_message(call.message.chat.id, 'Данная запись теперь невидна пользователям!', reply_markup=bttns)
            conn.commit()

    c.close()
    conn.close()


def change_data(message, a, b):
    global time_help
    global do_not_touch_or_this_bot_will_crash
    bttns = types.InlineKeyboardMarkup(row_width=2)
    do_not_touch_or_this_bot_will_crash = message.text
    btn1 = types.InlineKeyboardButton('Да', callback_data=f'Change_data, yes, {time_help[2]}, {b}')
    btn2 = types.InlineKeyboardButton('Нет', callback_data=f'Change_data, no, {time_help[2]}, {b}')
    bttns.add(btn1, btn2)
    alarm = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('К кружку', callback_data=f'{time_help[2]} 0%#admin')
    btn2 = types.InlineKeyboardButton('Повторить попытку', callback_data=f'Change_data, time, {time_help[2]}')
    btn3 = types.InlineKeyboardButton('К списку кружков', callback_data='Watch_all, page_1, remember')
    alarm.add(btn1, btn2, btn3)
    c = message.text
    err = False
    if b == 'time':
        if '$' not in c:
            if len(message.text.split()) >= 2:
                if len(message.text.split()[0].split("-")) >= 2:
                    c = f'\nВремя начала: {message.text.split()[0].split("-")[0]}\nВремя окончания: {message.text.split()[0].split("-")[1]}\nДень недели: {message.text.split()[1]}'
                else:
                    err = True
                    bot.send_message(message.chat.id,
                                     f'Данные указаны неверно! Ошибка: Missed {2 - len(message.text.split()[0].split("-"))} args* in >>[time start]-[time end]<< Пример: ([Время начала]-[Время окончания] [День недели в дательном падеже и мн. числе])',
                                     reply_markup=alarm)
            else:
                err = True
                bot.send_message(message.chat.id,
                                 f'Данные указаны неверно! Ошибка: Missed {2 - len(message.text.split())} args* in message. Пример: ([Время начала]-[Время окончания] [День недели в дательном падеже и мн. числе])',
                                 reply_markup=alarm)
        else:
            if len(message.text.split()) >= 4:
                if len(message.text.split()[1].split("-")) >= 2:
                    if len(message.text.split()[2].split("-")) >= 2:
                        c = f'''\n1 группа:\nВремя начала: {message.text.split()[1].split("-")[0]}\nВремя окончания: {message.text.split()[1].split("-")[1]}\n2 группа:\nВремя начала: {message.text.split()[2].split("-")[0]}\nВремя окончания: {message.text.split()[2].split("-")[1]}\nДень недели: {message.text.split()[3]}'''
                    else:
                        err = True
                        bot.send_message(message.chat.id,
                                         f'ERROR: missed {2 - len(message.text.split()[2].split("-"))} args* Вы должны следовать данной схеме: ($ [Время начала занятий 1-й группы]-[Время окончания занятий 1-й группы] [Время начала занятий 2-й группы]-[Время окончания занятий 2-й группы] [День недели в дательном падеже])',
                                         reply_markup=alarm)
                else:
                    err = True
                    bot.send_message(message.chat.id,
                                     f'ERROR: missed {2 - len(message.text.split()[1].split("-"))} args* Вы должны следовать данной схеме: ($ [Время начала занятий 1-й группы]-[Время окончания занятий 1-й группы] [Время начала занятий 2-й группы]-[Время окончания занятий 2-й группы] [День недели в дательном падеже])',
                                     reply_markup=alarm)
            else:
                err = True
                bot.send_message(message.chat.id,
                                 f'ERROR: missed {4 - len(message.text.split())} args* Вы должны следовать данной схеме: ($ [Время начала занятий 1-й группы]-[Время окончания занятий 1-й группы] [Время начала занятий 2-й группы]-[Время окончания занятий 2-й группы] [День недели в дательном падеже])',
                                 reply_markup=alarm)
    if not err:
        bot.send_message(message.chat.id, f'New {a}: {c}. Подтвердить изменения?', reply_markup=bttns)


def code_check(message):
    global admin
    if message.text == '7273131925':
        bttns = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton('Изменить список/структуру кружков', callback_data='all_positions, page_1, remember')
        btn2 = types.InlineKeyboardButton('Изменить пароль администратора', callback_data='Change_password')
        btn3 = types.InlineKeyboardButton('Выйти из аккаунта', callback_data='Logout')
        bttns.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, 'Регистрация успешно пройдена! Что желаете?', reply_markup=bttns)
        admin = True
    else:
        bot.send_message(message.chat.id, 'Неверный пароль! Попробовать еще раз: /login')


bot.infinity_polling()
