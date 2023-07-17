from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.incomes import Incomes
import datetime

from utils.pageination import pageination


def all_incomes(search, status, start_date, end_date, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Incomes.order_id.like(search_formatted)
    else:
        search_filter = Incomes.id > 0

    if status in [True,False]:
        status_filter = Incomes.status == status
    else:
        status_filter = Incomes.status.in_([True,False])

    try:
        if not start_date:
            start_date = datetime.date.min
        if not end_date:
            end_date = datetime.date.today()
        end_date = datetime.datetime.strptime(str(end_date),"%Y-%m-%d").date() + datetime.timedelta(days = 1)
    except Exception as error:
        raise HTTPException(status_code=400,detail="Faqat yyy-mmm-dd formatida yozing")
    dones = db.query(Incomes).filter(Incomes.date > start_date).filter(
        Incomes.date <= end_date).filter(search_filter,status_filter).order_by(Incomes.id.desc())
    if page and limit:
        return pageination(dones,page,limit)
    else:
        return dones.all()



def one_incomes(user_id, db):
    incomes = db.query(Incomes).filter(Incomes.user_id == user_id).first()
    return incomes



def add_incomes(form,user,db):
    if one_incomes(form.order_id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli order mavjud emas")
    if one_incomes(form.user_id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")
    new_incomes = Incomes(
        price = form.price,
        order_id = form.order_id,
        user_id = form.user_id
    )
    db.add(new_incomes)
    db.commit()
    db.refresh(new_incomes)
    return {"date":"Incomes saqlandi"}


def read_incomes(form,db,user):
    if one_incomes(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli income mavjud emas")
    incomes = db.query(Incomes).all()
    return incomes



def update_incomes(form,user,db):
    if one_incomes(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli order mavjud emas")
    number_verification = db.query(Incomes).filter(Incomes.user_id == form.user_id).first()
    if number_verification:
        raise HTTPException(status_code=400, detail="Bunday user_id  mavjud")
    income = db.query(Incomes).filter(Incomes.id == form.id).update(
        {
            Incomes.id:form.id,
            Incomes.price:form.price,
            Incomes.order_id:form.order_id,
            Incomes.user_id:user.id,
            Incomes.status:form.status,
        }
    )
    db.commit()
    return {"date":"Ma'lumot o'zgartirildi"}

def delete_incomes(id:int,user,db):
    income = db.query(Incomes).filter(Incomes.id==id).update(
        {
            Incomes.status:False
        }
    )
    db.commit()
    return {'date':"Ma'lumot o'chirildi"}


# def user_current(user, db):
#     return db.query(Incomes) .filter(Incomes.id == user.id).first()