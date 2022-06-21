from .base import BaseInterface
import requests


class UserInterface(BaseInterface):

    def __init__(self, token):
        super().__init__(token)
        self.url = self.url + "/user/"


    async def get_all(self):
        
        req = requests.get(self.url)

        return self.return_json(req, 200)

    async def get_by_id(self, user_id):

        url = self.url + str(user_id) + "/"

        req = requests.get(url)

        return self.return_json(req, 200)

    async def get_by_email(self, email):
        
        url = self.url + f"by_email/{email}"

        req = requests.get(url)

        return self.return_json(req, 200)


    async def get_by_telegram(self, telegram_id):
        
        url = self.url + f"by_telegram_id/{telegram_id}"

        req = requests.get(url)
        return self.return_json(req, 200)


    async def auth(self, email, passwd):
        
        url = self.url + "auth/"

        data = {
            "email" : email,
            "passwd" : passwd
        }

        req = requests.post(url, json=data)

        return self.return_json(req, 200)


    async def create(self, first_name, last_name, email, telegram_id, passwd):
        
        data = {
            "first_name" : first_name,
            "last_name" : last_name,
            "email" : email,
            "telegram_id" : telegram_id,
            "password" : passwd
        }

        req = requests.post(self.url, json=data)
        print(self.url)
        return self.return_json(req, 204)


    async def put(self, user_id, first_name, last_name, email, telegram_id, passwd):
        
        data = {
            "customer_sk" : user_id,
            "first_name" : first_name,
            "last_name" : last_name,
            "email" : email,
            "telegram_id" : telegram_id
        }

        req = requests.put(self.url, json=data)
        return self.return_json(req, 204)

    async def patch(self, user_id, first_name=None, last_name=None, email=None, telegram_id=None):
        
        data = {
            "customer_sk" : user_id
        }
        if first_name is not None:
            data['first_name'] = first_name
        if last_name is not None:
            data['last_name'] = last_name
        if email is not None:
            data['email'] = email
        if telegram_id is not None:
            data['telegram_id'] = telegram_id

        req = requests.patch(self.url, json=data)
        return self.return_json(req, 204)

    async def delete(self, user_id):
        
        data = {
            "customer_sk" : user_id
        }

        req = requests.delete(self.url, json=data)
        return self.return_json(req, 204)