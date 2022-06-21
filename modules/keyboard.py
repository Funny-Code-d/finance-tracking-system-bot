from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.types import KeyboardButton, InlineKeyboardButton
from collections import namedtuple


InlineKeyboardData = namedtuple("InlineKeyboardData", ["text", "callback"])

class Keyboard:
    
    
    @staticmethod
    def create_standart_keyboard(buttons_list: list) -> ReplyKeyboardMarkup:
        reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        reply_keyboard.add(*buttons_list)
        return reply_keyboard

    @staticmethod
    def create_inline_keyboard(*buttons_list: InlineKeyboardData) -> InlineKeyboardMarkup:
        markup_inline = InlineKeyboardMarkup(row_width=1)

        for item in buttons_list:
            markup_inline.insert(InlineKeyboardButton(text=item.text, callback_data=item.callback))
        return markup_inline

