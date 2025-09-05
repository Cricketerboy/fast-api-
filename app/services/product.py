from sqlalchemy.orm import Session
from app.schemas import product as schemas_product
from app.crud import product as crud_product

def get_products(db: Session):
    return crud_product.get_products(db)

def get_product(db: Session, product_id: int):
    return crud_product.get_product(db, product_id)

def create_product(db: Session, product: schemas_product.ProductCreate):
    return crud_product.create_product(db, product)

def update_product(db: Session, product_id: int, product: schemas_product.ProductCreate):
    return crud_product.update_product(db, product_id, product)

def delete_product(db: Session, product_id: int):
    return crud_product.delete_product(db, product_id)
