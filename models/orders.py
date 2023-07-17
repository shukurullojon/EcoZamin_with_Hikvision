from db import Base
from sqlalchemy import Column,Integer,String,Float,DateTime,func,Boolean,ForeignKey
from sqlalchemy.orm import relationship

class Orders(Base):
    __tablename__ = "Orders"
    id = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    date = Column(DateTime(timezone=True),default=func.now(),nullable=False)
    # customer_id = Column(Integer, ForeignKey("Customers.id"), nullable=False)
    user_id = Column(Integer,ForeignKey("Users.id"),nullable=False)
    status = Column(Boolean,default=True)
    owner = relationship('Users',back_populates='Qilingan_savdolar')

