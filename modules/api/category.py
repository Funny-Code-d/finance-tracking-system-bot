from .base import BaseInterface
from requests import get, post, put
from requests import delete as req_delete

class CategoryInterface(BaseInterface):

    def __init__(self, token):
        super().__init__(token)
        self.url = self.url + "/group/category/"

    async def get_all(self, user_id, group_id):
        params = {
            "customer_sk" : user_id,
            "group_sk" : group_id
        }
        req = get(self.url, params=params)
        return self.return_json(req, 200)

    async def add(self, user_id, group_id, category_name):
        data = {
            "customer_sk" : user_id,
            "group_sk" : group_id,
            "category_name" : category_name
        }
        print(data)
        req = post(self.url, json=data)
        return self.return_json(req, 200)

    async def put(self, user_id, group_id, category_id, category_name):
        
        data = {
            "customer_sk" : user_id,
            "group_sk" : group_id,
            "category_sk" : category_id,
            "category_name" : category_name
        }

        req = put(self.url, json=data)
        return self.return_json(req, 204)

    async def delete(self, user_id, group_id, category_id):
        data = {
            "customer_sk" : user_id,
            "group_sk" : group_id,
            "category_sk" : category_id
        }
