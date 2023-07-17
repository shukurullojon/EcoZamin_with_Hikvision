from pydantic import BaseModel
from pydantic.datetime_parse import date,datetime

class BacketBase(BaseModel):
    name:str
    quantity:int
    order_id:int
    user_id:int
    customer_id:str



class CreateBacket(BacketBase):
    pass



class UpdateBacket(BacketBase):
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