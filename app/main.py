from fastapi import FastAPI, Depends, HTTPException, Request, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
import db.crud as crud, models.models as models, db.schemas as schemas
from db.database import SessionLocal, engine
from typing import List

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables
def init_db():
    models.Base.metadata.create_all(bind=engine)

# Startup database
@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# Create customers
@app.post("/customers/create_customer", response_model=schemas.Customers)
def create_customer(customer: schemas.CustomersCreate, db: Session = Depends(get_db)):
    customer_code = customer.customer_code
    # Check if the customer_code already exists in the database
    existing_customer = db.query(models.Customers).filter(models.Customers.customer_code == customer_code).first()
    if existing_customer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Customer with the same customer_code already exists.")

    # If the customer_code does not exist, proceed with customer creation
    created_customer = crud.create_customers(db=db, customers_data=customer)
    created_customer_dict = created_customer.__dict__
    return created_customer_dict

@app.post("/customers/create_customer_new_user", response_model=List[schemas.Customers])
def create_customer_new_user(customer_request: schemas.CustomerCreateRequestBody, db: Session = Depends(get_db)):
    created_customers = crud.create_customers_new_user(db=db, customers_request=customer_request)

    if not created_customers:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Customers already exist for this user")

    return created_customers

# Get customers by user_id
@app.get("/customers/get_by_user_id/{user_id}", response_model=List[schemas.Customers])
def read_customers_by_user_id(user_id: str, db: Session = Depends(get_db)):
    db_customers = crud.get_customers_by_user_id(db=db, user_id=user_id)
    if db_customers is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customers

# Get customers by id
@app.get("/customers/get_by_id/{id}", response_model=schemas.Customers)
def read_customers_by_id(id: int, db: Session = Depends(get_db)):
    db_customer = crud.get_customer_by_id(db=db, id=id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

# Get all customers
@app.get("/customers/get_all_customers", response_model=List[schemas.Customers])
def read_all_customers(db: Session = Depends(get_db)):
    return crud.get_all_customers(db=db)

# Generate all customers
def generate_customers(db):
    init_db()
    crud.start_customer_scheduler(db=db)

db = SessionLocal()
generate_customers(db)
