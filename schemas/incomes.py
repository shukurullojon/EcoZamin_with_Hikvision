from pydantic import BaseModel
from pydantic.datetime_parse import date, datetime


class IncomesBase(BaseModel):
    price:int
    order_id : int
    user_id:int



class CreateIncomes(IncomesBase):
    pass


class UpdateIncomes(IncomesBase):
    id: int
    date: datetime
    status: bool = True


class UserCurrent(BaseModel):
    id:int
    name: str
    username: str
    password:str
    roll: str
    status: bool