from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from pydantic import ValidationError
from modules.keyboard import Keyboard
from modules.fs_machine import RegistState
from modules.models import Regist
from loader import dp, interface, orm



@dp.message_handler(commands=['menu', 'start'])
async def start_bot(message: Message):

    telegram_id = message.from_user.id
    print(telegram_id)
    is_regist = await orm.get_by_id(int(telegram_id))

    if is_regist:
        keyboard = [
            "Друзья",
            "Группы"
        ]
        kb = Keyboard.create_standart_keyboard(keyboard)

        await message.answer("Выберите вариант на клавиатуре", reply_markup=kb)
    else:
        keyboard = [
            "Регистрация",
            "Войти"
        ]
        kb = Keyboard.create_standart_keyboard(keyboard)

        await message.answer("Выберите вариант на клавиатуре", reply_markup=kb)
        await RegistState.action.set()

@dp.message_handler(state = RegistState.action)
async def get_action(message: Message, state: FSMContext):
    if (message.text == "Регистрация") or (message.text == "Войти"):
        await state.update_data({"action" : message.text})
        await message.answer("Введите вашу почту")
        await RegistState.email.set()
        
    else:
        await message.answer("Выберите варинат из клавиатуры")
        return

@dp.message_handler(state = RegistState.email)
async def get_email(message: Message, state: FSMContext):
    
    try:
        models = Regist(
            email=message.text
        )
        await state.update_data({"email" : message.text})
    except ValidationError:
        await message.answer("Введите корректную почту")
        return
    else:
        await message.answer("Ввведите пароль")
        await RegistState.passwd.set()


@dp.message_handler(state = RegistState.passwd)
async def get_passwd(message: Message, state: FSMContext):

    data = await state.get_data()
    action = data.get("action")
    email = data.get("email")

    keyboard_login = [
        "Друзья",
        "Группы"
    ]
    keyboard_failed = [
        "Регистрация",
        "Войти"
    ]
    kb = Keyboard.create_standart_keyboard(keyboard_failed)
    kb_login = Keyboard.create_standart_keyboard(keyboard_login)
    if action == "Регистрация":

        responce_api = await interface.User.create(
            message.from_user.first_name,
            message.from_user.last_name,
            email,
            message.from_user.id,
            message.text
        )

        if responce_api:
            await message.answer("Регистрация прошла успешно!", reply_markup=kb_login)
            await orm.create_user(
                 message.from_user.first_name,
                 message.from_user.last_name,
                 email,
                 message.from_user.id
            )
        else:
            
            await message.answer("Регистрация не удалась", reply_markup=kb)
    
    elif action == "Войти":

        responce_api = await interface.User.auth(email, message.text)

        if responce_api:
            await message.answer("Авторизация прошла успешно", reply_markup=kb_login)
            await orm.create_user(
                 message.from_user.first_name,
                 message.from_user.last_name,
                 email,
                 message.from_user.id
            )
        else:
            await message.answer("Авторизация не удалась, логин или пароль введён не верно", reply_markup=kb)
            
    
    else:
        await message.answer("Неизвестная ошибка, попробуйте ещё раз", reply_markup=kb)
    
    
    await state.finish()