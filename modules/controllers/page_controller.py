from telebot import types
from modules.controllers.street_controller import process_street


class PageSwitcher:
    def __init__(self, street_name, admin, db, message_id):
        if street_name == "profsoyuznaya":
            self.street_russian_name = "Профсоюзной"
        elif street_name == "lomonosovsky":
            self.street_russian_name = "Ломоносовском"
        else:
            self.street_russian_name = "Крижановского"
        self.message_id = message_id
        self.page_buttons = process_street(admin, db, street_name)
        self.page = 0
        self.max_page = len(self.page_buttons) // 5 - 1
        if self.max_page % 5:
            self.max_page += 1
        self.message_text = ["Кружки на ", self.street_russian_name,
                             ":\n", *[str(i) + ' ' for i in range(1, self.max_page + 2)]]

    def next_page(self):
        self.page += 1
        buttons, self.message_text = add_navigation_buttons(self.page, self.max_page, self.page_buttons, self.message_text)
        return buttons, ''.join(self.message_text)

    def prev_page(self):
        self.page -= 1
        buttons, self.message_text = add_navigation_buttons(self.page, self.max_page, self.page_buttons, self.message_text)
        return buttons, ''.join(self.message_text)

    def start_page(self):
        buttons, self.message_text = add_navigation_buttons(self.page, self.max_page, self.page_buttons,
                                                            self.message_text)
        return buttons, ''.join(self.message_text)


def add_navigation_buttons(page, max_page, page_buttons, message_text):
    buttons = types.InlineKeyboardMarkup()
    if page != 0:
        button_prev_page = types.InlineKeyboardButton(
            f"На стр. {page}", callback_data="Look_at_education_in, prev_page"
        )
    else:
        button_prev_page = types.InlineKeyboardButton(f"Главная", callback_data="main")
    if page != max_page:
        button_next_page = types.InlineKeyboardButton(
            f"На стр. {page + 2}", callback_data="Look_at_education_in, next_page"
        )
    else:
        button_next_page = types.InlineKeyboardButton(f"Главная", callback_data="main")

    buttons.row(
        button_prev_page,
        button_next_page
    )
    for el in page_buttons[page * 5:(page + 1) * 5]:
        buttons.row(
            el
        )
    if page != 0 and len(message_text[page + 2].split()) == 3:
        message_text[page + 2] = message_text[page + 2].split()[1]  # remove <b> format
        message_text[page + 2] = message_text[page + 2][1:-1] + " "  # remove "()"
    message_text[page + 3] = f"<b> ({message_text[page + 3][0]}) </b>"
    if page != max_page and len(message_text[page + 4].split()) == 3:
        print(message_text)
        print(max_page)
        print(message_text[page + 4].split()[1])
        message_text[page + 4] = message_text[page + 4].split()[1]  # remove <b> format
        message_text[page + 4] = message_text[page + 4][1:-1] + " "  # remove "()"

    return buttons, message_text
