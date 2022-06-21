from aiogram.types import Message, ReplyKeyboardRemove, callback_query
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from pydantic import ValidationError
from modules.keyboard import Keyboard
from modules.fs_machine import GroupsCommand, GroupsCreate, GroupsActionPurcahse
from modules.models import Regist
from loader import dp, interface, orm, pull_users
from modules.keyboard import InlineKeyboardData
from collections import namedtuple



@dp.callback_query_handler(state = GroupsActionPurcahse.action)
async def action_group(call: callback_query, state: FSMContext):

    answer = call.data

    if answer == "add":
        await call.message.answer("Отсканируйте чек и отправьте мне полученные данные", reply_markup=ReplyKeyboardRemove())
        await GroupsActionPurcahse.data_receipt.set()
    elif answer == "remove":
        pass


@dp.message_handler(state = GroupsActionPurcahse.data_receipt)
async def action_group(message: Message, state: FSMContext):

    receipt = message.text

    dataReceipt = namedtuple("DataReceipt", ["code", "data"])
    dataQrcode = data.split("&")
    listData = list()
    for item in dataQrcode:
        code, data = item.split("=")
        listData.append(dataReceipt(code, data))

    result = dict()
    for item in listData:
        result[item.code] = item.data

    data={
        'fn': str(result['fn']),
        'fd' : str(result['i']),
        'fp': str(result['fp']),
        't' : str(result['t']),
        'n' : str(result['n']),
        's' : str(result['s']),
        'qr' : '0',
    }

    await state.update_data({"data_receipt" : data})
    data_s = await state.get_data()
    customer_sk = data_s.get("customer_sk")
    group_sk = data_s.get("choise_group")


    
    category = await interface.Category.get_all(customer_sk, group_sk)
    if category:
        keyboard = list()
        answer_text = "Ваши категории:\n"
        for item in category['categories']:
            answer_text += f"   - {item['name_category']}\n"
            keyboard.append(InlineKeyboardData(item['name_category'], callback=item['category_sk']))
        
        keyboard = Keyboard.create_inline_keyboard(*keyboard)

        await message.edit_text("Выберите категорию", reply_markup=keyboard)
        await GroupsActionPurcahse.category.set()

@dp.callback_query_handler(state = GroupsActionPurcahse.category)
async def get_category_purchase(call: callback_query, state: FSMContext):

    data = await state.get_data()
    receipt = data.get("data_receipt")
    customer_sk = data.get("customer_sk")
    group_sk = data.get("choise_group")
    group = data.get("list_group")
    group_name = ""
    for item in group:
        if item['translit'] == group_sk:
            group_name = item['name_group']
            await state.update_data({"choise_group" : item['original']})
            break

    is_valid = await interface.Purchase.add(receipt, customer_sk, group_sk, call.data)
    if is_valid:
        keyboard = [
            InlineKeyboardData(text="Добавить покупку", callback='add_purchace'),
            InlineKeyboardData(text="Настроить список категорий", callback="category"),
            InlineKeyboardData(text="Настроить шаблоны отчетов", callback="templates"),
            InlineKeyboardData(text="Настройки группы", callback="settings"),
            InlineKeyboardData(text="Списки запланированных покупок", callback="todolist")
        ]
        keyboard = Keyboard.create_inline_keyboard(*keyboard)
        await call.message.answer("Покупка добавлена", reply_markup=ReplyKeyboardRemove())
        await call.message.answer(f"Группа: {group_name}\nВыберите", reply_markup=keyboard)
        await GroupsCommand.action.set()
