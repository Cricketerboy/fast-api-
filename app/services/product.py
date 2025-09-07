from sqlalchemy.orm import Session
from typing import Optional
from app.schemas import product as schemas_product
from app.crud import product as crud_product
from app.schemas.product import BulkProductCreate

def get_products(db: Session, id: Optional[int] = None, name: Optional[str] = None,
                 min_price: Optional[float] = None, max_price: Optional[float] = None):
    return crud_product.get_products(db, id=id, name=name, min_price=min_price, max_price=max_price)

def get_product(db: Session, product_id: int):
    return crud_product.get_product(db, product_id)

def create_product(db: Session, product: schemas_product.ProductCreate):
    return crud_product.create_product(db, product)

def update_product(db: Session, product_id: int, product: schemas_product.ProductCreate):
    return crud_product.update_product(db, product_id, product)

def delete_product(db: Session, product_id: int):
    return crud_product.delete_product(db, product_id)

def create_bulk_products(db: Session, bulk: BulkProductCreate):
    return crud_product.create_bulk_products(db, bulk)