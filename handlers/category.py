from unicodedata import category
from aiogram.types import Message, ReplyKeyboardRemove, callback_query
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from pydantic import ValidationError
from modules.keyboard import Keyboard
from modules.fs_machine import GroupsCommand, GroupsCreate, GroupsActionPurcahse, GroupActionCategory
from modules.models import Regist
from loader import dp, interface, orm, pull_users
from modules.keyboard import InlineKeyboardData


@dp.callback_query_handler(state = GroupActionCategory.action)
async def choise_category(call: callback_query, state: FSMContext):

    await call.answer(cache_time=0)
    answer = call.data

    state_data = await state.get_data()
    group_sk = state_data.get("groups")
    customer_sk = state_data.get("customer_sk")

    
    if answer == "add":
        await call.message.answer("Введите название категории", reply_markup=ReplyKeyboardRemove())
        await GroupActionCategory.name_category.set()
    elif answer == "remove":

        category = await interface.Category.get_all(customer_sk, group_sk)

        await state.update_data({"categories" : category['categories']})

        keyboard = list()
        for item in category['categories']:
            keyboard.append(
                InlineKeyboardData(item['name_category'], item['category_sk'])
            )
        keyboard = Keyboard.create_inline_keyboard(*keyboard)

        await call.message.answer("Выберите категорию которую нужно удалить", reply_markup=keyboard)
        await GroupActionCategory.delete_category.set()
    elif answer == "back":
        group_list = state_data.get('list_group')
        keyboard = list()
        for group in group_list:
            keyboard.append(InlineKeyboardData(text=group['name_group'], callback=group['translit']))
    
        keyboard.append(InlineKeyboardData(text="Создать группу", callback="CREATE_GROUP"))
        keyboard.append(InlineKeyboardData(text="Удалить группу", callback="DELETE_GROUP"))
        keyboard.append(InlineKeyboardData(text="Выход", callback="EXIT"))
        
        keyboard = Keyboard.create_inline_keyboard(*keyboard)

        await call.message.edit_text("Выерите", reply_markup=keyboard)
        await GroupsCommand.name_group.set()



@dp.message_handler(state = GroupActionCategory.name_category)
async def create_category(message: Message, state: FSMContext):

    # await call.answer(cache_time=0)
    answer = message.text

    state_data = await state.get_data()
    groups_sk = state_data.get("choise_group")
    customer_sk = state_data.get("customer_sk")
    
    is_valid = await interface.Category.add(customer_sk, groups_sk, answer)

    
    keyboard = [
        InlineKeyboardData(text="Добавить покупку", callback='add_purchace'),
        InlineKeyboardData(text="Настроить список категорий", callback="category"),
        InlineKeyboardData(text="Настроить шаблоны отчетов", callback="templates"),
        InlineKeyboardData(text="Настройки группы", callback="settings"),
        InlineKeyboardData(text="Списки запланированных покупок", callback="todolist")
    ]
    keyboard = Keyboard.create_inline_keyboard(*keyboard)


    if is_valid:
        await message.answer("Категория добавлена", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Категория не добавлена", reply_markup=ReplyKeyboardRemove())


    await message.answer("Выберите что нужно сделать", reply_markup=keyboard)
    await GroupsCommand.action.set()


@dp.callback_query_handler(state = GroupActionCategory.delete_category)
async def delete_category(call: callback_query, state: FSMContext):

    answer = call.data

    state_data = await state.get_data()

    categories = state_data.get("categories")
    group_sk = state_data.get("choise_group")
    customer_sk = state_data.get("customer_sk")

    if answer in categories:
        is_valid = await interface.Category.delete(customer_sk, group_sk, answer)
        keyboard = [
            InlineKeyboardData(text="Добавить покупку", callback='add_purchace'),
            InlineKeyboardData(text="Настроить список категорий", callback="category"),
            InlineKeyboardData(text="Настроить шаблоны отчетов", callback="templates"),
            InlineKeyboardData(text="Настройки группы", callback="settings"),
            InlineKeyboardData(text="Списки запланированных покупок", callback="todolist")
        ]
        keyboard = Keyboard.create_inline_keyboard(*keyboard)

        if is_valid:
            await call.message.answer("Категория удалена", reply_markup=ReplyKeyboardRemove)
        else:
            await call.message.answer("Категория не удалена", reply_markup=ReplyKeyboardRemove)
            
    
        await call.message.answer("Выберите действие", reply_markup=keyboard)
        await GroupsCommand.action.set()

    else:
        await call.message.answer("Повторите ввод", reply_markup=ReplyKeyboardRemove)
        return




    