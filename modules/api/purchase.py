from .base import BaseInterface
from requests import post, request
from requests import delete as req_delete

class PurchaseInterface(BaseInterface):

    def __init__(self, token):
        super().__init__(token)
        self.url = self.url + "/purchase/"

    async def add(self, data_receipt, user_id, group_id, category_id):
        
        data = {
            "fn" : data_receipt['fn'],
            "fd" : data_receipt['fd'],
            "fp" : data_receipt['fp'],
            "t" : data_receipt['t'],
            "n" : data_receipt['n'],
            "amount" : data_receipt['s'],
            "customer_sk" : user_id,
            "group_id" : group_id,
            "category_id" : category_id
        }

        req = post(self.url, json=data)
        return self.return_json(req, 200)

    async def delete(self, user_id, group_id, purchase_id):
        
        data = {
            "customer_sk" : user_id,
            "group_id" : group_id,
            "purchase_id" : purchase_id
        }

        req = req_delete(self.url, json=data)
        return self.return_json(req, 204)