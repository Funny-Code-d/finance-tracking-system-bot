from aiogram.types import Message, ReplyKeyboardRemove, callback_query
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from pydantic import ValidationError
from modules.keyboard import Keyboard
from modules.fs_machine import GroupsCommand, GroupsCreate, GroupsActionPurcahse, GroupActionCategory, GroupActionTemplates
from modules.models import Regist
from loader import dp, interface, orm, pull_users
from modules.keyboard import InlineKeyboardData
from transliterate import translit

@dp.message_handler(commands=['groups'])
async def get_menu(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    if telegram_id in pull_users:
        user = await orm.get_by_id(telegram_id)
        groups = await interface.Group.get_all(user['customer_sk'])


        list_groups = list()
        list_local_group_sk = list()
        index_grop = "G"
        for item in groups['groups']:
            
            list_groups.append({
                "original" : item['group_sk'],
                "translit" : index_grop,
                "name_group" : item["name_group"],
                "access" : item["access"],
                "description" : item['description']
            })
            list_local_group_sk.append(index_grop)
            index_grop += "G"
        await state.update_data({
                "list_group" : list_groups,
                "list_local_group_sk" : list_local_group_sk
            })


        keyboard = list()
        if len(groups['groups']) > 0:
            
            for group in list_groups:
                keyboard.append(InlineKeyboardData(text=group['name_group'], callback=group['translit']))
        
            keyboard.append(InlineKeyboardData(text="Создать группу", callback="CREATE_GROUP"))
            keyboard.append(InlineKeyboardData(text="Удалить группу", callback="DELETE_GROUP"))
            keyboard.append(InlineKeyboardData(text="Выход", callback="EXIT"))
            
            keyboard = Keyboard.create_inline_keyboard(*keyboard)

            await message.answer("Выерите", reply_markup=keyboard)
        
        if len(groups['groups']) == 0:
            keyboard.append(InlineKeyboardData(text="Создать группу", callback="CREATE_GROUP"))
            keyboard = Keyboard.create_inline_keyboard(*keyboard)
            await message.answer("У вас ещё нет групп, давайте создадим первую", reply_markup=keyboard)

        await GroupsCommand.name_group.set()        

    else:
        await message.answer("Вы не авторизованны, введите /start")

@dp.callback_query_handler(state = GroupsCommand.name_group)
async def choise_group(call: callback_query, state: FSMContext):

    await call.answer(cache_time=0)
    answer = call.data
    state_data = await state.get_data()
    groups_sk = state_data.get("list_local_group_sk")
    group = state_data.get('list_group')
    group_name = ""
    for item in group:
        if item['translit'] == answer:
            group_name = item['name_group']
            await state.update_data({"choise_group" : item['original']})
            break
    
    user = await orm.get_by_id(call.from_user.id)

    await state.update_data({
        "group_sk" : answer,
        "customer_sk" : user['customer_sk']
    })
    
    if answer == "CREATE_GROUP":
        await call.message.answer("Введите название для новой группы")
        await GroupsCreate.name_group.set()
    elif answer == "DELETE_GROUP":
        pass
    elif answer in groups_sk:
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
    elif answer == "EXIT":
        await state.finish()
        await call.message.answer("/friends - Список друзей\n/groups - Список групп", reply_markup=ReplyKeyboardRemove())
    else:
        await call.message.answer("Повторите ввод")


@dp.callback_query_handler(state = GroupsCommand.action)
async def action_group(call: callback_query, state: FSMContext):

    answer = call.data
    data_state = await state.get_data()
    group_sk = data_state.get("choise_group")
    customer_sk = data_state.get("customer_sk")

    if answer == "add_purchace":
        keyboard = [
            InlineKeyboardData(text="Добавить покупку", callback="add"),
            InlineKeyboardData(text="Удалить покупку", callback="remove"),
        ]
        keyboard = Keyboard.create_inline_keyboard(*keyboard)
        await call.message.edit_text("Выберите действие", reply_markup=keyboard)
        await GroupsActionPurcahse.action.set()
    elif answer == "category":
        
        
        category = await interface.Category.get_all(customer_sk, group_sk)
        if category:
            answer_text = "Ваши категории:\n"
            for item in category['categories']:
                answer_text += f"   - {item['name_category']}\n"
            answer_text += "\n\nВыберите что сделать"

            keyboard = [
                InlineKeyboardData("Создать категорию", "add"),
                InlineKeyboardData("Удалить категорию", "remove"),
                InlineKeyboardData("Назад", "back")
            ]
            keyboard = Keyboard.create_inline_keyboard(*keyboard)

            await call.message.edit_text(answer_text, reply_markup=keyboard)
            await GroupActionCategory.action.set()
    elif answer == "templates":
        

        templates = await interface.Template.get_all(customer_sk, group_sk)

        if templates:
            data_templates = list()
            answer_text = "Ваши шаблоны отчётов:\n"
            for item in templates['items']:
                answer_text += f"\n{item['name_template']}\nКоличество дней - {item['number_days']}\nКатегории:\n"
                data_category = list()
                for item_category in item['categories']:
                    answer_text += f"    {item_category['name_category']}\n"
                    data_category.append(item_category['name_category'])
                data_templates.append({
                    "template_sk" : item['template_sk'],
                    "name_template" : item['name_template'],
                    "number_days" : item['number_days'],
                    "categories" : data_category
                })
                answer_text += "\n"
            
            keyboard = [
                InlineKeyboardData("Создать шаблон отчёта", "add"),
                InlineKeyboardData("Удалить шаблон отчёта", "remove"),
                InlineKeyboardData("Назад", "back")
            ]
            keyboard = Keyboard.create_inline_keyboard(*keyboard)
            await call.message.edit_text(answer_text, reply_markup=keyboard)
            await GroupActionTemplates.action.set()
                

    elif answer == "settings":
        pass
    elif answer == "todolist":
        pass
    elif answer == "back":
        await GroupsCommand.display.set()

        group_list = data_state.get('list_group')
        keyboard = list()
        for group in group_list:
            keyboard.append(InlineKeyboardData(text=group['name_group'], callback=group['translit']))
    
        keyboard.append(InlineKeyboardData(text="Создать группу", callback="CREATE_GROUP"))
        keyboard.append(InlineKeyboardData(text="Удалить группу", callback="DELETE_GROUP"))
        keyboard.append(InlineKeyboardData(text="Выход", callback="EXIT"))
        
        keyboard = Keyboard.create_inline_keyboard(*keyboard)

        await call.message.edit_text("Выерите", reply_markup=keyboard)
        await GroupsCommand.name_group.set()

