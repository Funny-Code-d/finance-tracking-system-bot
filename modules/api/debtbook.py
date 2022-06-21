from .base import BaseInterface
from requests import get, post
from requests import delete as req_delete

class DebtbookInterface(BaseInterface):

    def __init__(self, token):
        super().__init__(token)
        self.url = self.url + "/debtbook/"

    async def get_all(self, user_id):
        url = self.url + f"{user_id}/"
        req = get(url)
        return self.return_json(req, 200)
    
    async def get_history(self, user_id, debtor_id):
        url = self.url + f"{user_id}/history/{debtor_id}/"
        req = get(url)
        return self.return_json(req, 200)

    async def add_debtor(self, user_id, debtor_name, teleram_id, first_name, last_name):
        data = {
            "customer_sk" : user_id,
            "debtor_name" : debtor_name,
            "telegram_id" : teleram_id,
            "first_name" : first_name,
            "last_name" : last_name,
        }

        req = post(self.url, json=data)
        return self.return_json(req, 200)

    async def add_transaction(self, user_id, debtor_id, type_action, transaction, amount):
        url = self.url + "regist"

        data = {
            "customer_sk" : user_id,
            "debtor_sk" : debtor_id,
            "type_action" : type_action,
            "transaction" : transaction,
            "amount" : amount
        }

        req = post(url, json=data)
        return self.return_json(req, 200)

    async def delete(self, user_id, debtor_id):

        data = {
            "customer_sk" : user_id,
            "debtor_sk" : debtor_id
        }

        req = req_delete(self.url, json=data)
        return self.return_json(req, 200)