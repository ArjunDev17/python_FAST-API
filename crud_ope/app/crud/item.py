# crud/item.py
from sqlalchemy.orm import Session
from app.models.item import Item

def create_item(db: Session, name: str, description: str):
    db_item = Item(name=name, description=description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()
