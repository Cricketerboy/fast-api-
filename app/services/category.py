from sqlalchemy.orm import Session
from app.schemas import category as schemas_category
from app.crud import category as crud_category

def get_categories(db: Session):
    return crud_category.get_categories(db)

def get_category(db: Session, category_id: int):
    return crud_category.get_category(db, category_id)

def create_category(db: Session, category: schemas_category.CategoryCreate):
    return crud_category.create_category(db, category)
