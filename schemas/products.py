from pydantic import BaseModel
from pydantic.datetime_parse import date,datetime

class ProductBase(BaseModel):
    name:str
    birlik:str
    old_price:int
    new_price:int
    type:str
    rasm: str


class CreateProduct(ProductBase):
    pass


class UpdateProduct(ProductBase):
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