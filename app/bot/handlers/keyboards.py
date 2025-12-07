from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/add 100 food")],
            [KeyboardButton(text="/today"), KeyboardButton(text="/month")],
        ],
        resize_keyboard=True,
    )

