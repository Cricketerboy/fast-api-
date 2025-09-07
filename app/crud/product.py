from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.product import Product
from typing import Optional
from app.schemas.product import ProductCreate, BulkProductCreate

def get_products(db: Session, id: Optional[int] = None, name: Optional[str] = None,
                 min_price: Optional[float] = None, max_price: Optional[float] = None):
    query = db.query(Product).filter(Product.is_deleted == False)  

    if id is not None:
        query = query.filter(Product.id == id)
    if name is not None:
        query = query.filter(Product.name.ilike(f"%{name}%"))
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    return query.all()

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_product_by_name(db: Session, name: str):
    return db.query(Product).filter(Product.name == name).first()

def create_product(db: Session, product: ProductCreate):
    
    existing = get_product_by_name(db, product.name)
    if existing:
        
        return None

    db_product = Product(**product.dict())
    db.add(db_product)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        
        return None
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: ProductCreate):
    db_product = get_product(db, product_id)
    if not db_product:
        return None

    
    if product.name != db_product.name:
        clash = get_product_by_name(db, product.name)
        if clash and clash.id != product_id:
            return None

    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity
    db_product.category_id = product.category_id

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return None
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)
    if not db_product:
        return False
    db_product.is_deleted = True  
    db.commit()
    return True

def create_bulk_products(db: Session, bulk: BulkProductCreate):
    product_names = [p.name for p in bulk.products]

    # check duplicates within the request
    if len(product_names) != len(set(product_names)):
        return None, "Duplicate product names in request payload"

    # check against DB
    existing = db.query(Product).filter(Product.name.in_(product_names)).all()
    if existing:
        existing_names = [e.name for e in existing]
        return None, f"Products already exist: {', '.join(existing_names)}"

    db_products = [Product(**p.dict()) for p in bulk.products]
    db.add_all(db_products)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        return None, f"Integrity error: {str(e)}"

    for prod in db_products:
        db.refresh(prod)
    return db_products, None
