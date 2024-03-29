import sqlite3

from telebot import types
import modules.controllers.routes_controller as routes_controller
from modules.instances.bot_instance import bot


admin = False
ADMIN_PASSWORD = "7273131925"


def check_user(message):
    """Check user"""
    bot.send_message(message.chat.id, "Введите пароль: ")
    bot.register_next_step_handler(message, check_password)


def check_password(message):
    """Fn to check user password"""
    global admin

    if message.text == ADMIN_PASSWORD:
        buttons = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton(
            "Изменить список/структуру кружков",
            callback_data="all_positions, page_1, remember",
        )
        btn2 = types.InlineKeyboardButton(
            "Изменить пароль администратора", callback_data="change_password"
        )
        btn3 = types.InlineKeyboardButton("Выйти из аккаунта", callback_data="logout")
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
    """Starts bot"""
    bttns = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(
        "Дополнительное образование", callback_data="dop_education"
    )
    btn2 = types.InlineKeyboardButton("Контактные данные", callback_data="contacts")
    bttns.add(btn1, btn2)
    bot.send_message(
        message.chat.id,
        "Здравствуйте! Я бот Лицея №1533 и могу ответить на ваши вопросы. Ниже представлены разделы, которые в меня "
        "загружены. Если вам нужна помощь воспользуйтесь командой /help.",
        reply_markup=bttns,
    )


def show_help(message):
    """Handles show help command"""
    markup = types.InlineKeyboardMarkup(row_width=1)
    item = types.InlineKeyboardButton("Контактные данные", callback_data="contacts")
    item2 = types.InlineKeyboardButton("Главное меню", callback_data="main")
    markup.row(item, item2)
    item3 = types.InlineKeyboardButton(
        "Как записаться на доп. образование", callback_data="how_to_register"
    )
    markup.row(item3)
    bot.send_message(
        message.chat.id,
        "Данный бот предназначен для предоставления информации о дополнительном образовании. Если вы не нашли здесь "
        "нужных вам данных, обратитесь к администрации лицея (контактные данные откроются при нажатии на кнопку "
        "ниже) или воспользуйтесь разделом 'Наша учеба' на сайте www.lit.msu.ru.\n\nВоспользуйтесь командой "
        "/main или кнопкой под сообщением для возвпащения к главным опциям.",
        reply_markup=markup,
    )


def callback_handler(call):
    """Handles all bot commands"""
    command = call.data
    conn = sqlite3.connect("data")
    db = conn.cursor()

    match command:
        case "main":
            routes_controller.main_handler(call, bot)
        case "contacts":
            routes_controller.contacts_handler(call, bot)
        case "admin":
            routes_controller.admin_page_handler(call, bot)
        case "how_to_register":
            routes_controller.how_to_register_handler(call, bot)
        case "dop_education":
            routes_controller.dop_education_handler(call, bot)
        case "change_password":
            # not implemented
            routes_controller.change_password_handler(call, bot)
            routes_controller.add_handler(call, bot)
        case "logout":
            # not implemented
            routes_controller.logout_handler(call, bot)
        case "holidays":
            routes_controller.holidays_handler(bot, call)
        case _ as tag if "Look_at_education_in" in tag:
            routes_controller.look_at_education_handler(call, bot, admin, db)
        case _ as par if "edit" in par:
            routes_controller.edit_handler(call, bot, db, conn)
        case _ as detail if "position_details" in detail:
            routes_controller.position_details_handler(call, bot, admin, db)
        case _ as korp if "add" in korp:
            routes_controller.create_data_handler(call, bot, db, conn)
        case _ as teststring if "all_positions" in teststring:
            routes_controller.all_positions_handler(call, bot, admin, db)
        case _:
            routes_controller.main_handler(call, bot)

    db.close()
    conn.close()
