from aiogram.dispatcher.filters.state import StatesGroup, State

class RegistState(StatesGroup):
    action = State()
    email = State()
    passwd = State()

class RefreshState(StatesGroup):
    email = State()
    refresh_token = State()
    responce_new_token = State()

