from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.db import get_db
from app.schemas import product as schemas_product
from app.services import product as service_product

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=List[schemas_product.ProductResponse])
def read_products(
    id: Optional[int] = None,
    name: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db),
):
    return service_product.get_products(db, id=id, name=name, min_price=min_price, max_price=max_price)
@router.get("/get", response_model=schemas_product.ProductResponse)
def read_product(id: int, db: Session = Depends(get_db)):
    product = service_product.get_product(db, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=schemas_product.ProductResponse)
def create_product(product: schemas_product.ProductCreate, db: Session = Depends(get_db)):
    created = service_product.create_product(db, product)
    if not created:
       
        raise HTTPException(
            status_code=400,
            detail=f"Product '{product.name}' already exists (belongs to another category)."
        )
    return created



@router.put("/update", response_model=schemas_product.ProductResponse)
def update_product(id: int, product: schemas_product.ProductCreate, db: Session = Depends(get_db)):
    updated = service_product.update_product(db, id, product)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

@router.delete("/delete")
def delete_product(id: int, db: Session = Depends(get_db)):
    success = service_product.delete_product(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

@router.post("/bulk", response_model=List[schemas_product.ProductResponse])
def create_bulk_products(bulk: schemas_product.BulkProductCreate, db: Session = Depends(get_db)):
    products, error = service_product.create_bulk_products(db, bulk)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return products