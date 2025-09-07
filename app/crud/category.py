from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category import CategoryCreate

def get_categories(db: Session):
    return db.query(Category).all()

def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()

def get_category_by_name(db: Session, name: str):
    return db.query(Category).filter(Category.name == name).first()

def create_category(db: Session, category: CategoryCreate):
    existing = get_category_by_name(db, category.name)
    if existing:
        return None
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category
