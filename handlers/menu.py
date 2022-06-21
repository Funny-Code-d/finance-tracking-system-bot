from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from pydantic import ValidationError
from modules.keyboard import Keyboard
from modules.fs_machine import RegistState
from modules.models import Regist
from loader import dp, interface, orm, pull_users


@dp.message_handler(commands=['menu'])
async def get_menu(message: Message):
    if message.from_user.id in pull_users:
        await message.answer("/groups")
    else:
        await message.answer("Вы не авторизованны, введите /start")