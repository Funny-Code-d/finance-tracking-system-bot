from .base import BaseInterface
from requests import get, post
from requests import delete as req_delete 

class ToDoListInterface(BaseInterface):

    def __init__(self, token):
        super().__init__(token)
        self.url = self.url + "/todo/"

    async def get_all(self, user_id, group_id):
        params = {
            "customer_sk" : user_id,
            "group_sk" : group_id
        }

        req = get(self.url, params=params)
        return self.return_json(req, 200)

    async def add(self, user_id, group_id, name_todolist, items):
        
        data = {
            "customer_sk" : user_id,
            "group_sk" : group_id,
            "name_todolist" : name_todolist,
            "items" : items
        }

        req = post(self.url, json=data)
        return self.return_json(req, 204)

    async def delete(self, user_id, group_id, todolist_id):
        
        data = {
            "customer_sk" : user_id,
            "group_sk" : group_id,
            "todo_list_sk" : todolist_id
        }
        req = req_delete(self.url, json=data)
        return self.return_json(req, 204)

    async def add_item(self, user_id, group_id, todolist_id, name_item, price_item, quantity_item):
        
        data = {
            "customer_sk" : user_id,
            "group_sk" : group_id,
            "todo_list_sk" : todolist_id,
            "name_item" : name_item,
            "price_item" : price_item,
            "quantity_item" : quantity_item
        }
        url = self.url + "item/"
        req = post(url, json=data)
        return self.return_json(req, 204)

    async def delete_item(self, user_id, group_id, todolist_id, item_todolist_id):
        data = {
            "customer_sk" : user_id,
            "group_sk" : group_id,
            "todo_list_sk" : todolist_id,
            "item_todo_list_sk" : item_todolist_id
        }

        url = self.url + "/item/"
        req = req_delete(url, json=data)
        return self.return_json(req, 204)

    async def complited_item(self, user_id, group_id, todolist_id, item_todolist_id):
        data = {
            "customer_sk" : user_id,
            "group_sk" : group_id,
            "todo_list_sk" : todolist_id,
            "item_todo_list_sk" : item_todolist_id
        }

        url = self.url + "/item/complited/"
        req = post(url, json=data)
        return self.return_json(req, 204)