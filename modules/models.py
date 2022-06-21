from pydantic import BaseModel, EmailStr
from typing import Optional


class Regist(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    passwd: Optional[str]