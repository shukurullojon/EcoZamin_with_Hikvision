
from passlib.context import CryptContext
from sqlalchemy.orm import joinedload

from models.orders import Orders

pwd_context=CryptContext(schemes=['bcrypt'])

from fastapi import HTTPException
from models.users import Users

from routes.auth import get_password_hash
from utils.pageination import pageination


def all_users(search, status, roll, page, limit, db):
	if search:
		search_formatted="%{}%".format(search)
		search_filter=Users.name.like(search_formatted) | Users.number.like(search_formatted) | Users.username.like(
			search_formatted) | Users.roll.like(search_formatted)
	else:
		search_filter=Users.id > 0
	if status in [True, False]:
		status_filter=Users.status == status
	else:
		status_filter=Users.id > 0
	
	if roll:
		roll_filter=Users.roll == roll
	else:
		roll_filter=Users.id > 0
	
	# users=db.query(Users).options(joinedload(Users.kpi), joinedload(Users.order.and_(Orders.status==True))).filter(search_filter, status_filter, roll_filter).order_by(Users.name.asc())
	users = db.query(Users).options( joinedload(Users.Qilingan_xarajatlar)).options( joinedload(Users.Qilingan_savdolar)).options( joinedload(Users.Keltirilgan_foyda)).filter(search_filter, status_filter, roll_filter).order_by(Users.id.desc())
	if page and limit:
		return pageination(users, page, limit)
	else:
		return users.all()






def one_user(id, db):
	return db.query(Users).filter(Users.id == id).first()


def user_current(user, db):
	return db.query(Users) .filter(Users.id == user.id).first()

def create_user(form, user, db):
	user_verification=db.query(Users).filter(Users.username == form.username).first()
	if user_verification:
		raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud")
	number_verification=db.query(Users).filter(Users.number == form.number).first()
	if number_verification:
		raise HTTPException(status_code=400, detail="Bunday telefon raqami  mavjud")

	new_user_db=Users(
		name=form.name,
		username=form.username,
		number=form.number,
		password=get_password_hash(form.password),
		roll=form.roll,
		status=form.status,
	
	)
	db.add(new_user_db)
	db.commit()
	db.refresh(new_user_db)

	return new_user_db


def update_user(form, user, db):
	if one_user(form.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
	user_verification=db.query(Users).filter(Users.username == form.username).first()
	if user_verification and user_verification.id != form.id:
		raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud")

	db.query(Users).filter(Users.id == form.id).update({
		Users.name: form.name,
		Users.username: form.username,
		Users.password: get_password_hash(form.password),
		Users.roll: form.roll,
		Users.status: form.status,
		Users.number: form.number,
		
	})
	db.commit()


	return one_user(form.id, db)


def update_user_salary(id, salary,db):
	if one_user(id, db) is None:
		raise HTTPException(status_code=400, detail=f"Bunday {id} raqamli hodim mavjud emas")
	
	db.query(Users).filter(Users.id == id).update({
		Users.salary: salary,
		
	})
	db.commit()
	return one_user(id, db)




def user_delete(id, db):
	if one_user(id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli ma'lumot mavjud emas")
	db.query(Users).filter(Users.id == id).update({
		Users.status: False,
	})
	db.commit()
	return {"date": "Ma'lumot o'chirildi !"}







