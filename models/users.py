from sqlalchemy import Column, Integer, String, Boolean,Float,Text
from sqlalchemy.orm import relationship

from db import Base




class Users(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    roll = Column(String(20), nullable=False)
    name = Column(String(20), nullable=False)
    number = Column(String(20), nullable=False)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    token = Column(String(400), default='',nullable=True)
    Qilingan_savdolar = relationship('Orders',back_populates='owner')
    mahsulotlar = relationship('Products',back_populates='mahsulot')
    Keltirilgan_foyda = relationship('Incomes', back_populates='daromad')
    Qilingan_xarajatlar = relationship('Expenses', back_populates='xarajat')



