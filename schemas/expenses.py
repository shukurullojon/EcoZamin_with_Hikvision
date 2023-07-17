from pydantic import BaseModel
from pydantic.datetime_parse import date, datetime


class ExpensesBase(BaseModel):
    price:int
    worker_id:int
    source:str
    comment:str
    user_id:int


class CreateExpenses(ExpensesBase):
    pass



class UpdateExpenses(ExpensesBase):
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