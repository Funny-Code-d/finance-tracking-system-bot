from aiogram.types import Message, ReplyKeyboardRemove, callback_query
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from pydantic import ValidationError
from modules.keyboard import Keyboard
from modules.fs_machine import GroupsCommand, GroupsCreate
from modules.models import Regist
from loader import dp, interface, orm, pull_users
from modules.keyboard import InlineKeyboardData


@dp.message_handler(state = GroupsCreate.name_group)
async def create_group_name(message: Message, state: FSMContext):

    await state.update_data({
        "name_new_group" : message.text
    })
    keyboard = [
        InlineKeyboardData(text='Личная', callback="private"),
        InlineKeyboardData(text="Общая", callback="public")
    ]
    keyboard = Keyboard.create_inline_keyboard(*keyboard)
    await message.answer("Выберите тип группы", reply_markup=keyboard)
    await GroupsCreate.access.set()


@dp.callback_query_handler(state = GroupsCreate.access)
async def create_group_name(call: callback_query, state: FSMContext):

    await state.update_data({
        "access_new_group" : call.data
    })
    
    await call.message.answer("Введите описание группы", reply_markup=ReplyKeyboardRemove())
    await GroupsCreate.description.set()



@dp.message_handler(state = GroupsCreate.description)
async def create_group_name(message: Message, state: FSMContext):

    data = await state.get_data()
    name_group = data.get("name_new_group")
    access = data.get("access_new_group")
    description = message.text
    user = await orm.get_by_id(message.from_user.id)
    is_valid = await interface.Group.create(user['customer_sk'], name_group, access, description)
    keyboard = [
        "/friends",
        "/groups"
    ]
    kb = Keyboard.create_standart_keyboard(keyboard)
    if is_valid:
        await message.answer("Группа создана, введите /groups", reply_markup=kb)
    else:
        await message.answer("Группа не создана", reply_markup=kb)

    await state.finish()