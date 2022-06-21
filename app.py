from aiogram import executor
from aiogram.dispatcher import FSMContext
from loader import dp
import handlers
from db.base import database

async def startup(dispatcher):
    await database.connect()

async def shutdown(dispatcher):
    await database.disconnect()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=startup, on_shutdown=shutdown)
