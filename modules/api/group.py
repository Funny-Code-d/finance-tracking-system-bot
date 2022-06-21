from requests import get, post, put, patch
from requests import delete as req_delete
from .base import BaseInterface


class GroupInterface(BaseInterface):

    def __init__(self, token):

        super().__init__(token)
        self.url = self.url + "/group/"

    async def get_all(self, user_id):
        
        url = self.url + f"{user_id}/"
        req = get(url)
        return self.return_json(req, 200)


    async def get_by_id(self, user_id, group_id):
        
        url = self.url + f"{user_id}/{group_id}/"
        req = get(url)
        return self.return_json(req, 200)

    async def create(self, user_id, name_group, access, description):
        
        data = {
            "name_group" : name_group,
            "access" : access,
            "description" : description,
            "customer_sk" : user_id
        }
        req = post(self.url, json=data)
        return self.return_json(req, 204)

    async def put(self, user_id, name_group, group_id, access, description):
        
        data = {
            "customer_sk" : user_id,
            "group_sk" : group_id,
            "group_name" : name_group,
            "access" : access,
            "desciption" : description
        }

        req = put(self.url, json=data)
        return self.return_json(req, 204)

    async def patch(self, user_id, group_id, name_group=None, access=None, description=None):
        
        data = {
            "customer_sk" : user_id,
            "group_sk" : group_id
        }
        if name_group is not None:
            data['group_name'] = name_group
        if access is not None:
            data['access'] = access
        if description is not None:
            data['description'] = description
        
        req = patch(self.url, json=data)
        return self.return_json(req, 204)

    async def delete(self, user_id, group_id):
        
        data = {
            "customer_sk" : user_id,
            "group_sk" : group_id
        }

        req = req_delete(self.url, json=data)
        return self.return_json(req, 204)
