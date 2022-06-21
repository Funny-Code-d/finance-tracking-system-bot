from aiogram.dispatcher.filters.state import StatesGroup, State

class RegistState(StatesGroup):
    action = State()
    email = State()
    passwd = State()

class RefreshState(StatesGroup):
    email = State()
    refresh_token = State()
    responce_new_token = State()

class GroupsCommand(StatesGroup):
    name_group = State()
    action = State()
    display = State()
    exit = State()

class GroupsCreate(StatesGroup):
    name_group = State()
    access = State()
    description = State()

class GroupsActionPurcahse(StatesGroup):
    action = State()
    data_receipt = State()
    category = State()

class GroupActionCategory(StatesGroup):
    delete_category = State()
    name_category = State()
    action = State()

class GroupActionTemplates(StatesGroup):
    name_templates = State()
    action = State()

class GroupActionTemplatesCreate(StatesGroup):
    name_template = State()
    number_days = State()
    categories = State()

class GroupActionStatistics(StatesGroup):
    type_out = State()
    name_template = State()

class GroupActionSettings(StatesGroup):
    access = State()

class GroupActionToDo(StatesGroup):
    action = State()

