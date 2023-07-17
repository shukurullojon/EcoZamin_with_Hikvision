from pydantic import BaseModel
from pydantic.datetime_parse import date,datetime

class CustomersBase(BaseModel):
    name:str
    phone:int
    address:str




class CreateCustomer(CustomersBase):
    date:datetime


class UpdateCustomer(CustomersBase):
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