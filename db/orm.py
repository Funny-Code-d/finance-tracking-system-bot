from .base import database
from .table import customers

class ORMDatabase:

    def __init__(self):
        self.database = database

    async def get_by_id(self, telegram_id):

        query = customers.select().where(
            customers.c.telegram_id==telegram_id
        )

        responce_db = await self.database.fetch_one(query=query)

        if responce_db:
            return {
                "first_name" : responce_db['first_name'],
                "last_name" : responce_db['last_name'],
                "telegram_id" : responce_db['telegram_id'],
                "email" : responce_db['email']
            }
        else:
            return False

    async def create_user(self, first_name, last_name, email, telegram_id):

        values = {
            "first_name" : first_name,
            "last_name" : last_name,
            "email" : email,
            "telegram_id" : telegram_id
        }
        query = customers.insert().values(**values)
        await self.database.execute(query=query)
        return True