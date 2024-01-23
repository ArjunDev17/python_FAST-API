# database/crud.py
# database/crud.py
from sqlalchemy.orm import Session
# from .models import Customer  # Update this line to import the Customer model correctly
from models.customer import Customer 
def create_customer(db: Session, customer_data):
    new_customer = Customer(**customer_data.dict())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

def get_customer(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id).first()

def get_customers(db: Session):
    return db.query(Customer).all()

# from sqlalchemy.orm import Session
# from . import models

# def create_customer(db: Session, customer_data):
#     new_customer = models.Customer(**customer_data.dict())
#     db.add(new_customer)
#     db.commit()
#     db.refresh(new_customer)
#     return new_customer

# def get_customer(db: Session, customer_id: int):
#     return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

# def get_customers(db: Session):
#     return db.query(models.Customer).all()
