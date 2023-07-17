from pydantic import BaseModel
from pydantic.datetime_parse import date,datetime

class OrdersBase(BaseModel):
    user_id:int

class CreateOrders(OrdersBase):
    pass



class UpdateOrders(OrdersBase):
    id:int
    date: datetime
    status: bool = True



class UserCurrent(BaseModel):
    id:int
    name: str
    username: str
    password:str
    roll: str
    status: bool