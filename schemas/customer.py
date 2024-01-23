# schemas/customer.py
from pydantic import BaseModel

class CreateCustomer(BaseModel):
    name: str
    email: str

class CustomerResponse(BaseModel):
    id: int
    name: str
    email: str
