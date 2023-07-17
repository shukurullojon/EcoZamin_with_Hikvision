from pydantic import BaseModel
from pydantic.datetime_parse import date,datetime


class TypeBase(BaseModel):
    name:str
    date:datetime


class CreateType(TypeBase):
    pass


class UpdateType(TypeBase):
    id:int
    status:bool=True
    date: datetime



class UserCurrent(BaseModel):
    id:int
    name: str
    username: str
    password:str
    roll: str
    status: bool