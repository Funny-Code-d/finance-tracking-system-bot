import requests
from .api.user import UserInterface
from .api.group import GroupInterface
from .api.purchase import PurchaseInterface
from .api.category import CategoryInterface
from .api.templates import TemplatesInterface
from .api.todolist import ToDoListInterface
from .api.debtbook import DebtbookInterface


class ApiInterface:

    def __init__(self, token):
        self.token = token
        self.User = UserInterface(token)
        self.Group = GroupInterface(token)
        self.Purchase = PurchaseInterface(token)
        self.Category = CategoryInterface(token)
        self.Template = TemplatesInterface(token)
        self.ToDoList = ToDoListInterface(token)
        self.Debtbook = DebtbookInterface(token)