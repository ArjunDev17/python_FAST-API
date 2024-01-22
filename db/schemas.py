from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class CustomersBase(BaseModel):
    name: str
    mobileNumber: str
    typesOfCustomer: str
    address: str
    
    gstNumber: str
    created_date: datetime
    last_updated_date: Optional[datetime] = None

class CustomersCreate(CustomersBase):
    pass

class Customers(CustomersBase):
    id: int

    class Config:
        orm_mode = True

class CustomerCreateRequestBody(BaseModel):
    user_id: str
    center: str
