from db import SessionLocal
from fastapi import FastAPI
# from fastapi_utils.tasks import repeat_every
from sqlalchemy.orm import Session


from routes import   users,auth,products,products_types,orders,customers,backet,expenses,incomes
from db import Base, engine
import datetime



Base.metadata.create_all(bind=engine)

app=FastAPI(
	title="FastApi",
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
	CORSMiddleware,
	allow_origins=['*'],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


@app.get('/')
def home():
	return {"message": "Salom hammaga"}


app.include_router(
	auth.login_router,
	prefix='/auth',
	tags=['User auth section'],
	responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
	           401: {'desription': 'Unauthorized'}}
)

app.include_router(
	users.router_user,
	prefix='/user',
	tags=['User section'],
	responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
	           401: {'desription': 'Unauthorized'}}
)





app.include_router(
    router=products.user_router,
    tags=["Products bo'limi"],
    prefix='/products'
)


app.include_router(
    router=products_types.user_router,
    tags=["Types bo'limi"],
    prefix='/types'
)


app.include_router(
    router=orders.user_router,
    tags=["Orders bo'limi"],
    prefix='/orders'
)




app.include_router(
    router=customers.user_router,
    tags=["Customers bo'limi"],
    prefix='/customers'
)


app.include_router(
    router=backet.user_router,
    tags=["Backet bo'limi"],
    prefix='/backet'
)


app.include_router(
    router=expenses.user_router,
    tags=["Expenses bo'limi"],
    prefix='/expenses'
)



app.include_router(
    router=incomes.user_router,
    tags=["Incomes bo'limi"],
    prefix='/incomes'
)




