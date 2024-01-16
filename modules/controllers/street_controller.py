from telebot import types


def process_street(admin, db, street_name):
    if street_name == "profsoyuznaya":
        street_str = "на Профсоюзной"
    elif street_name == "lomonosovsky":
        street_str = "на Ломоносовском"
    else:
        street_str = "на Крижановского"

    bttns = types.InlineKeyboardMarkup()

    positions = [el for el in db.execute(
        "SELECT * FROM dop_ed WHERE korp = ?", [street_str]
    ).fetchall() if el[0] < 10000 or admin]

    if not positions == []:
        for position in positions:
            if len(str(position[2]).split()) > 1:
                bttns.add(
                    types.InlineKeyboardButton(
                        f'{position[1]} для {", ".join(str(position[2]).split()[0:-1])} и {str(position[2]).split()[-1]} классов',
                        callback_data=f"{position[0]} position_details",
                    )
                )
            else:
                bttns.add(
                    types.InlineKeyboardButton(
                        f"{position[1]} для {str(position[2]).split()[-1]} классов",
                        callback_data=f"{position[0]} position_details",
                    )
                )

    if admin:
        bttns.row(
            types.InlineKeyboardButton(
                "Добавить запись", callback_data=f"add, {street_str}"
            )
        )
    bttns.row(
        types.InlineKeyboardButton("Главная", callback_data="main"),
    )

    if not positions == []:
        return bttns
    else:
        return False
