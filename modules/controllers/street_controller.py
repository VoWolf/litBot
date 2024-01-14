from telebot import types


def process_street(call, bot, admin, db, street_name):
    if street_name == "profsoyuznaya":
        street_str = "на Профсоюзной"
    elif street_name == "lomonosovsky":
        street_str = "на Ломоносовском"
    else:
        street_str = "на Крижановского"

    positions = [el for el in db.execute(
        "SELECT * FROM dop_ed WHERE korp = ?", [street_str]
    ).fetchall() if el[0] < 10000 or admin]

    # positions = db.execute(
    #     "SELECT * FROM dop_ed WHERE korp = ?", [street_str]
    # ).fetchall()

    bttns = types.InlineKeyboardMarkup()
    if admin:
        bttns.row(
            types.InlineKeyboardButton(
                "Добавить запись", callback_data=f"add, {street_str}"
            )
        )
    bttns.row(
        types.InlineKeyboardButton("Главная", callback_data="restart"),
        types.InlineKeyboardButton("Помощь", callback_data="help"),
    )
    if positions == []:
        bot.send_message(
            call.message.chat.id,
            f"К сожалению, кружков {street_str} не добавлено!",
            reply_markup=bttns,
        )
    else:
        for el in positions:
            if len(str(el[2]).split()) > 1:
                bttns.add(
                    types.InlineKeyboardButton(
                        f'{el[1]} для {", ".join(str(el[2]).split()[0:-1])} и {str(el[2]).split()[-1]} классов',
                        callback_data=f"{el[0]} position_details",
                    )
                )
            else:
                bttns.add(
                    types.InlineKeyboardButton(
                        f"{el[1]} для {str(el[2]).split()[-1]} классов",
                        callback_data=f"{el[0]} position_details",
                    )
                )
        bot.send_message(
            call.message.chat.id, f"Кружки {street_str}:", reply_markup=bttns
        )
