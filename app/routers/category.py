from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.schemas import category as schemas_category
from app.services import category as service_category

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model=list[schemas_category.CategoryResponse])
def read_categories(db: Session = Depends(get_db)):
    return service_category.get_categories(db)

@router.get("/get", response_model=schemas_category.CategoryResponse)
def read_category(id: int, db: Session = Depends(get_db)):
    category = service_category.get_category(db, id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/", response_model=schemas_category.CategoryResponse)
def create_category(category: schemas_category.CategoryCreate, db: Session = Depends(get_db)):
    created = service_category.create_category(db, category)
    if not created:
        raise HTTPException(status_code=400, detail="Category already exists")
    return created
