import datetime

from fastapi import APIRouter,Depends
from pydantic.datetime_parse import date
from sqlalchemy.orm import Session
from db import get_db
from functions.customers import *
from routes.auth import get_current_active_user
from schemas.customers import CustomersBase, CreateCustomer, UpdateCustomer, UserCurrent

user_router = APIRouter()


@user_router.post("/add")
def customer_qoshish(form:CreateCustomer,db:Session=Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)):
    return add_customers(form=form,user=current_user,db=db)

@user_router.get('/',  status_code = 200)
def get_users(search:str=None,status:bool=True,id:int=0,start_date:date=datetime.datetime.now().date().min,end_date:date=datetime.datetime.now().date(),page:int=1,limit:int=2, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_customer(id, db)
    else :
        return all_customers(search=search,status=status,start_date=start_date,end_date=end_date,page=page,limit=limit,db=db)


# @user_router.get('/user',  status_code = 200)
# def get_user_current(db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
#     if current_user:
#         return user_current(current_user, db)


@user_router.put("/update")
def customer_update(form:UpdateCustomer,db:Session=Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)):
    return update_customer(form=form,user=current_user,db=db)


@user_router.delete("/delete")
def customer_delete(id:int,db:Session=Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)):
    return delete_customer(id=id,user=current_user,db=db)