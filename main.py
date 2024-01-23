
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.customer import CreateCustomer, CustomerResponse
from database.database import engine, SessionLocal
from database import crud  # Add this line
from typing import List
app = FastAPI()

# Dependency to get the SQLAlchemy session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to create a customer
@app.post("/customers/", response_model=CustomerResponse)
async def create_customer(customer_data: CreateCustomer, db: Session = Depends(get_db)):
    new_customer = crud.create_customer(db, customer_data)
    return CustomerResponse(id=new_customer.id, name=new_customer.name, email=new_customer.email)

# Endpoint to get a specific customer by ID
@app.get("/customers/{customer_id}", response_model=CustomerResponse)
async def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = crud.get_customer(db, customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return CustomerResponse(id=customer.id, name=customer.name, email=customer.email)

# Endpoint to get all customers
@app.get("/customers/", response_model=List[CustomerResponse])
async def get_customers(db: Session = Depends(get_db)):
    customers = crud.get_customers(db)
    return [CustomerResponse(id=customer.id, name=customer.name, email=customer.email) for customer in customers]
