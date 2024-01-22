from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Customers(Base):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True, index=True)
    mobileNumber = Column(String(255),unique=True)
    name = Column(String(255))
    typesOfCustomer=Column(String(255))
    address = Column(String(255))
    gstNumber=Column(String(255))
    created_date = Column(DateTime)
    last_updated_date = Column(DateTime, nullable=True)
