from pydantic import BaseModel
from typing import Optional


class ProductBase(BaseModel):
    name: str
    category: Optional[str] = None
    buying_price: Optional[float] = 0
    selling_price: Optional[float] = 0
    quantity_sold: Optional[int] = 0
    current_stock: Optional[int] = 0


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True


class SaleCreate(BaseModel):
    product_id: int
    quantity: int


class DashboardOut(BaseModel):
    profit_today: int
    profit_change: int
    attention_count: int
    best_product: dict
    top_products: list


class RecommendationOut(BaseModel):
    id: int
    type: str
    title: str
    detail: str
    productId: Optional[int]
