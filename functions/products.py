from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.products import Products
import datetime

from utils.pageination import pageination


def all_products(search, status, start_date, end_date, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Products.name.like(search_formatted)|\
                        Products.new_price.like(search_formatted)|\
                        Products.type.like(search_formatted)|\
                        Products.birlik.like(search_formatted)|\
                        Products.old_price.like(search_formatted)|\
                        Products.rasm.like(search_formatted)
    else:
        search_filter = Products.id > 0

    if status in [True,False]:
        status_filter = Products.status == status
    else:
        status_filter = Products.status.in_([True,False])

    try:
        if not start_date:
            start_date = datetime.date.min
        if not end_date:
            end_date = datetime.date.today()
        end_date = datetime.datetime.strptime(str(end_date),"%Y-%m-%d").date() + datetime.timedelta(days = 1)
    except Exception as error:
        raise HTTPException(status_code=400,detail="Faqat yyy-mmm-dd formatida yozing")
    dones = db.query(Products).options( joinedload(Products.mahsulot)).filter(Products.date > start_date).filter(
        Products.date <= end_date).filter(search_filter,status_filter).order_by(Products.id.desc())
    if page and limit:
        return pageination(dones,page,limit)
    else:
        return dones.all()



def add_product(form,user,db):
    user_verification = db.query(Products).filter(Products.name == form.name).first()
    if user_verification and user_verification.id != form.id:
        raise HTTPException(status_code=400, detail="Bunday nomdagi mahsulot mavjud")
    new_product = Products(
        name = form.name,
        old_price = form.old_price,
        new_price = form.new_price,
        type = form.type,
        birlik = form.birlik,
        user_id = user.id,
        rasm = form.rasm,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"date":"Mahsulot saqlandi"}


def read_products(db,form):
    if one_product(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli mahsulot mavjud emas")
    products = db.query(Products).all()
    return products

def one_product(id:int, db):
    product = db.query(Products).filter(Products.id == id).first()
    return product

def update_product(form,user,db):
    if one_product(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli mahsulot mavjud emas")
    product = db.query(Products).filter(Products.id == form.id).update(
        {
            Products.id:form.id,
            Products.name:form.name,
            Products.birlik:form.birlik,
            Products.rasm:form.rasm,
            Products.new_price:form.new_price,
            Products.old_price:form.old_price,
            Products.type:form.type,
            Products.status:form.status,
        }
    )
    db.commit()
    return {"date":"Ma'lumot o'zgartirildi"}

def delete_product(id:int,user,db):
    product = db.query(Products).filter(Products.id==id).update(
        {
            Products.status:False
        }
    )
    db.commit()
    return {'date':"Ma'lumot o'chirildi"}



# def user_current(user, db):
#     return db.query(Products) .filter(Products.id == user.id).first()