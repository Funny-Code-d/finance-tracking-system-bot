from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from pydantic import ValidationError
from modules.keyboard import Keyboard
from modules.fs_machine import RegistState
from modules.models import Regist
from loader import dp, interface, orm, pull_users


@dp.message_handler(commands=['help'])
async def get_menu(message: Message):
    answer = ""
    await message.answer(answer)