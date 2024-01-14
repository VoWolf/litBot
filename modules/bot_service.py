import telebot
from telebot import types

bot = telebot.TeleBot("6438520666:AAFmH9T9S8B3XmpEyQ4UXZWDWF4DBliDfL4")

admin = False
admin_password = "7273131925"


def check_user(message):
    bot.send_message(message.chat.id, "Введите пароль: ")
    bot.register_next_step_handler(message, check_password)


def check_password(message):
    global admin

    if message.text == admin_password:
        buttons = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton(
            "Изменить список/структуру кружков",
            callback_data="all_positions, page_1, remember",
        )
        btn2 = types.InlineKeyboardButton(
            "Изменить пароль администратора", callback_data="Change_password"
        )
        btn3 = types.InlineKeyboardButton("Выйти из аккаунта", callback_data="Logout")
        buttons.add(btn1, btn2, btn3)
        bot.send_message(
            message.chat.id,
            "Регистрация успешно пройдена! Что желаете?",
            reply_markup=buttons,
        )
        admin = True
    else:
        bot.send_message(
            message.chat.id, "Неверный пароль! Попробовать еще раз: /login"
        )


def start(message):
    buttons = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(
        "Дополнительное образование", callback_data="main_1"
    )
    btn2 = types.InlineKeyboardButton("Контактные данные", callback_data="main_2")
    btn3 = types.InlineKeyboardButton("Помощь", callback_data="help")
    buttons.add(btn1, btn2, btn3)
    bot.send_message(
        message.chat.id,
        "Здравствуйте! Я бот Лицея №1533 и могу ответить на ваши вопросы. Вот разделы которые в меня "
        "загружены:",
        reply_markup=buttons,
    )


def show_help(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item = types.InlineKeyboardButton(
        "Контактные данные", callback_data="main_question_2"
    )
    item2 = types.InlineKeyboardButton("Главное меню", callback_data="restart")
    item3 = types.InlineKeyboardButton(
        "Как записаться на доп. образование", callback_data="how_to_register?"
    )
    markup.add(item, item2, item3)
    bot.send_message(
        message.chat.id,
        "Данный бот предназначен для предоставления информации о дополнительном образовании. Если вы не нашли здесь "
        "нужной вам информации, обратитесь к администрации лицея (контактные данные откроются при нажатии на кнопку "
        "ниже) \n \n Воспользуйтесь командой /start или кнопкой под сообщением для возвпащения к главным опциям.",
        reply_markup=markup,
    )
