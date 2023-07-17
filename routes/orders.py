from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from db import get_db
from functions.orders import *
from routes.auth import get_current_active_user
from schemas.orders import CreateOrders, UpdateOrders, OrdersBase, UserCurrent
from pydantic.datetime_parse import date
user_router = APIRouter()


@user_router.post("/add")
def order_qoshish(form:CreateOrders,db:Session=Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)):
    return add_orders(form=form,user=current_user,db=db)

@user_router.get('/',  status_code = 200)
def get_users(search:str=None,status:bool=True,id:int=0,start_date:date=datetime.datetime.now().date().min,end_date:date=datetime.datetime.now().date(),page:int=1,limit:int=2, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_order(id, db)
    else :
        return all_orders(search=search,status=status,start_date=start_date,end_date=end_date,page=page,limit=limit,db=db)


# @user_router.get('/user',  status_code = 200)
# def get_user_current(db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
#     if current_user:
#         return user_current(current_user, db)


@user_router.put("/update")
def order_update(form:UpdateOrders,db:Session=Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)):
    return update_order(form=form,user=current_user,db=db)


@user_router.delete("/delete")
def order_delete(id:int,db:Session=Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)):
    return delete_order(id=id,user=current_user,db=db)