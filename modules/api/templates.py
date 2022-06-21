from .base import BaseInterface
from requests import get, patch, post, put
from requests import delete as req_delete

class TemplatesInterface(BaseInterface):

    async def get_all(self, user_id, group_id):
        params = {
            "customer_sk" : user_id,
            "group_sk" : group_id
        }

        req = get(self.url, params=params)
        return self.return_json(req, 200)

    async def add(self, user_id, group_id, name_template, number_days, categories):
        data = {
            "name_template" : name_template,
            "number_days" : number_days,
            "customer_sk" : user_id,
            "group_sk" : group_id,
            "categories" : categories
        }

        req = post(self.url, json=data)
        return self.return_json(req, 204)

    async def patch(self, user_id, group_id, template_id, name_template=None, number_days=None, categories=None):
        
        data = {
            "customer_sk" : user_id,
            "group_sk" : group_id,
            "template_sk" : template_id
        }

        if name_template is not None:
            data['name_template'] = name_template

        if number_days is not None:
            data['number_days'] = number_days
        
        if categories is not None:
            data['categories'] = categories

        req = patch(self.url, json=data)
        return self.return_json(req, 204)

    async def delete(self, user_id, group_id, template_id):
        
        data = {
            "customer_sk" : user_id,
            "group_sk" : group_id,
            "template_sk" : template_id
        }

        req = req_delete(self.url, json=data)
        return self.return_json(req, 204)