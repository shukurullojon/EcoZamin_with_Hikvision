from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from pydantic.datetime_parse import date
from db import get_db
from functions.products import *
from routes.auth import get_current_active_user
from schemas.products import ProductBase, CreateProduct, UpdateProduct, UserCurrent
import datetime
user_router = APIRouter()


@user_router.post("/add")
def product_qoshish(form:CreateProduct,db:Session=Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)):
    return add_product(form=form,user=current_user,db=db)

@user_router.get('/',  status_code = 200)
def get_users(search:str=None,status:bool=True,id:int=0,start_date:date=datetime.datetime.now().date().min,end_date:date=datetime.datetime.now().date(),page:int=1,limit:int=2, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_product(id, db)
    else :
        return all_products(search=search,status=status,start_date=start_date,end_date=end_date,page=page,limit=limit,db=db)


# @user_router.get('/user',  status_code = 200)
# def get_user_current(db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
#     if current_user:
#         return user_current(current_user, db)


@user_router.put("/update")
def product_update(form:UpdateProduct,db:Session=Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)):
    return update_product(form=form,user=current_user,db=db)


@user_router.delete("/delete")
def product_delete(id:int,db:Session=Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)):
    return delete_product(id=id,user=current_user,db=db)