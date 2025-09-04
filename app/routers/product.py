from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.crud import product as crud_product
from app.schemas import product as schemas_product

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=list[schemas_product.ProductResponse])
def read_products(db: Session = Depends(get_db)):
    return crud_product.get_products(db)

@router.get("/{product_id}", response_model=schemas_product.ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = crud_product.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=schemas_product.ProductResponse)
def create_product(product: schemas_product.ProductCreate, db: Session = Depends(get_db)):
    return crud_product.create_product(db, product)

@router.put("/{product_id}", response_model=schemas_product.ProductResponse)
def update_product(product_id: int, product: schemas_product.ProductCreate, db: Session = Depends(get_db)):
    updated = crud_product.update_product(db, product_id, product)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    success = crud_product.delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

