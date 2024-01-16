import modules.services.bot_service as bot_service
from modules.instances.bot_instance import bot
from db.database import *

create_tables()


@bot.message_handler(commands=["admin", "login", "reg"])
def check_user(message):
    bot_service.check_user(message)


@bot.message_handler(commands=["start"])
def start(message):
    bot_service.start(message)


@bot.message_handler(commands=["help"])
def help_message(message):
    bot_service.show_help(message)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    bot_service.callback_handler(call)


bot.infinity_polling()
