from aiogram.types import Message, ReplyKeyboardRemove, callback_query
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from pydantic import ValidationError
from modules.keyboard import Keyboard
from modules.fs_machine import GroupActionTemplatesCreate, GroupsCommand, GroupsCreate, GroupActionTemplates
from modules.models import Regist
from loader import dp, interface, orm, pull_users
from modules.keyboard import InlineKeyboardData


@dp.callback_query_handler(state = GroupActionTemplates.action)
async def action_teplates(call: callback_query, state: FSMContext):

    answer = call.data

    data = await state.get_data()
    customer_sk = data.get("customer_sk")
    group_sk = data.get("choise_group")
    

    if answer == "add":
        await call.message.answer("Введиет название для нового шаблона отчёта", reply_markup=ReplyKeyboardRemove())
        await GroupActionTemplatesCreate.name_template.set()
    elif answer == "remove":
        pass
    elif answer == "back":
        group_name = ""
        group = data.get("list_group")
        for item in group:
            if item['translit'] == group_sk:
                group_name = item['name_group']
                # await state.update_data({"choise_group" : item['original']})
                break
        keyboard = [
            InlineKeyboardData(text="Добавить покупку", callback='add_purchace'),
            InlineKeyboardData(text="Настроить список категорий", callback="category"),
            InlineKeyboardData(text="Настроить шаблоны отчетов", callback="templates"),
            InlineKeyboardData(text="Настройки группы", callback="settings"),
            InlineKeyboardData(text="Списки запланированных покупок", callback="todolist"),
            InlineKeyboardData(text="Назад", callback="back")
        ]
        keyboard = Keyboard.create_inline_keyboard(*keyboard)
        await call.message.edit_text(f"Группа: {group_name}\nВыберите что нужно сделать", reply_markup=keyboard)
        await GroupsCommand.action.set()
    else:
        return

@dp.message_handler(state = GroupActionTemplatesCreate.name_template)
async def get_name_template(message: Message, state: FSMContext):

    await state.update_data({
        "name_new_template" : message.text
    })

    await message.answer("Введите количество дней.\nЗа сколько дней от даты построения отчёта, брать данные.")
    await GroupActionTemplatesCreate.number_days.set()

@dp.message_handler(state = GroupActionTemplatesCreate.number_days)
async def get_number_days(message: Message, state: FSMContext):
    data = await state.get_data()
    customer_sk = data.get("customer_sk")
    group_sk = data.get("choise_group")
    try:
        await state.update_data({
            "number_days_new_templates" : int(message.text)
        })
    except ValueError:
        await message.answer("Введите число")
        return
    else:
        categories = await interface.Category.get_all(customer_sk, group_sk)

        if categories:
            list_categories = list()
            keyboard = list()
            for item in categories['categories']:
                list_categories.append({
                    "category_sk" : item['category_sk'],
                    "name_category" : item['name_category'],
                    "is_add" : False
                })
                keyboard.append(InlineKeyboardData(item["name_category"], item['category_sk']))
            keyboard.append(InlineKeyboardData("Готово", callback="success"))
            keyboard = Keyboard.create_inline_keyboard(*keyboard)

            await state.update_data({
                "categories_new_tempate" : list_categories
            })
            await message.answer("Выберите категории которые включить в шаблон отчёта\n\n", reply_markup=keyboard)
            await GroupActionTemplatesCreate.categories.set()

@dp.callback_query_handler(state = GroupActionTemplatesCreate.categories)
async def get_categories_templates(call: callback_query, state: FSMContext):

    answer = call.data
    data = await state.get_data()

    list_categories = data.get("categories_new_tempate")

    if answer == "success":
        add_category = list()
        for item in list_categories:
            if item['is_add']:
                add_category.append(item['category_sk'])
        
        customer_sk = data.get("customer_sk")
        group_sk = data.get("choise_group")
        name_template = data.get("name_new_template")
        number_days = data.get("number_days_new_templates")
        is_valid = await interface.Template.add(customer_sk, group_sk, name_template, number_days, add_category)
        if is_valid:
            keyboard = [
                InlineKeyboardData(text="Добавить покупку", callback='add_purchace'),
                InlineKeyboardData(text="Настроить список категорий", callback="category"),
                InlineKeyboardData(text="Настроить шаблоны отчетов", callback="templates"),
                InlineKeyboardData(text="Настройки группы", callback="settings"),
                InlineKeyboardData(text="Списки запланированных покупок", callback="todolist")
            ]
            keyboard = Keyboard.create_inline_keyboard(*keyboard)
            await call.message.edit_text("Новый шаблон создан", reply_markup=keyboard)
            await GroupsCommand.action.set()
    
    
    else:
        answer_text = "Выберите категории которые включить в шаблон отчёта\n\n"
        keyboard = list()
        for item in list_categories:
            if item['category_sk'] == int(answer):
                item['is_add'] = not item['is_add']
                # print(item)
                if item['is_add']:
                    answer_text += f" -   {item['name_category']}\n"
            else:
                if item['is_add']:
                    answer_text += f" -   {item['name_category']}\n"
            keyboard.append(InlineKeyboardData(item["name_category"], item['category_sk']))
        keyboard.append(InlineKeyboardData("Готово", callback="success"))
        answer_text += "\n\n"
        keyboard = Keyboard.create_inline_keyboard(*keyboard)

        
        await state.update_data({
            "categories_new_tempate" : list_categories
        })

        await call.message.edit_text(answer_text, reply_markup=keyboard)
        # print(list_categories)
        await GroupActionTemplatesCreate.categories.set()
