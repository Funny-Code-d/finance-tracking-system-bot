from aiogram import executor
from aiogram.dispatcher import FSMContext
from loader import dp, orm, pull_users
import handlers
from db.base import database

async def update_pull_users():
    pull_users.clear()

    users = await orm.get_pull_users()

    for u in users:
        pull_users.append(u)
    print("Список пользователей после обновления: ", pull_users)


async def startup(dispatcher):
    await database.connect()
    users = await orm.get_pull_users()

    for u in users:
        pull_users.append(u)
    print("Список пользователей после запуска:", pull_users)


async def shutdown(dispatcher):
    await database.disconnect()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=startup, on_shutdown=shutdown)
