from pydantic import BaseModel
from typing import List, Optional

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int = 0
    category_id: int

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    class Config:
        orm_mode = True

# 👇 bulk create wrapper
class BulkProductCreate(BaseModel):
    products: List[ProductCreate]
