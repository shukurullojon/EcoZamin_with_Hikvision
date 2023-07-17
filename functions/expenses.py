from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.expenses import Expenses
import datetime

from utils.pageination import pageination


def all_expenses(search, status, start_date, end_date, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Expenses.price.like(search_formatted)|\
                        Expenses.source.like(search_formatted)|Expenses.worker_id.like(search_formatted)
    else:
        search_filter = Expenses.id > 0

    if status in [True,False]:
        status_filter = Expenses.status == status
    else:
        status_filter = Expenses.status.in_([True,False])

    try:
        if not start_date:
            start_date = datetime.date.min
        if not end_date:
            end_date = datetime.date.today()
        end_date = datetime.datetime.strptime(str(end_date),"%Y-%m-%d").date() + datetime.timedelta(days = 1)
    except Exception as error:
        raise HTTPException(status_code=400,detail="Faqat yyy-mmm-dd formatida yozing")
    dones = db.query(Expenses).filter(Expenses.date > start_date).filter(
        Expenses.date <= end_date).filter(search_filter,status_filter).order_by(Expenses.id.desc())
    if page and limit:
        return pageination(dones,page,limit)
    else:
        return dones.all()





def add_expenses(form,user,db):
    if one_expense(form.user_id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli ma'lumot qo'shib bo'lmaydi, qayta urining")
    new_expenses = Expenses(
        price = form.price,
        worker_id = form.worker_id,
        source = form.source,
        user_id = form.user_id,
        comment = form.comment,
    )
    db.add(new_expenses)
    db.commit()
    db.refresh(new_expenses)
    return {"date":"Expenses saqlandi"}


def read_expenses(db,user):
    expenses = db.query(Expenses).all()
    return expenses

def one_expense(user_id, db):
    expense = db.query(Expenses).filter(Expenses.user_id == user_id).first()
    return expense

def update_expenses(form,user,db):
    if one_expense(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli expenses mavjud emas")
    user_verification = db.query(Expenses).filter(Expenses.user_id == form.user_id).first()
    if user_verification and user_verification.id != form.id:
        raise HTTPException(status_code=400, detail="Bunday nomdagi foydalanuvchi mavjud")
    expenses = db.query(Expenses).filter(Expenses.id == form.id).update(
        {
            Expenses.id:form.id,
            Expenses.price:form.price,
            Expenses.worker_id:form.worker_id,
            Expenses.source:form.source,
            Expenses.comment:form.comment,
            Expenses.user_id:form.user_id,
            Expenses.status:form.status,
        }
    )
    db.commit()
    return {"date":"Ma'lumot o'zgartirildi"}

def delete_expense(id:int,user,db):
    expense = db.query(Expenses).filter(Expenses.id==id).update(
        {
            Expenses.status:False
        }
    )
    db.commit()
    return {'date':"Ma'lumot o'chirildi"}


# def user_current(user, db):
#     return db.query(Expenses) .filter(Expenses.id == user.id).first()