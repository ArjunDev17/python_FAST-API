# api/item.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud.item import create_item, get_item

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_item_api(name: str, description: str, db: Session = Depends(get_db)):
    return create_item(db, name=name, description=description)

@router.get("/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = get_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
