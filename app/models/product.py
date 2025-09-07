from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.db import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    # make name globally unique
    name = Column(String, nullable=False, unique=True)
    description = Column(String)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    category = relationship("Category", back_populates="products")

    is_deleted = Column(Boolean, default=False)

    


    

