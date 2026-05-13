from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class UserBase(BaseModel):
    login: str
    full_name: str
    role: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    article: str
    name: str
    category: Optional[str] = None
    description: Optional[str] = None
    manufacturer: Optional[str] = None
    supplier: Optional[str] = None
    price: float = Field(ge=0)
    unit: Optional[str] = None
    quantity_in_stock: int = Field(ge=0)
    discount_percent: int = Field(ge=0, le=100)
    image_path: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    article: str
    status: str
    pickup_point_id: int
    order_date: date
    issue_date: Optional[date] = None
    user_id: Optional[int] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderBase):
    pass


class Order(OrderBase):
    id: int

    class Config:
        orm_mode = True


class PickupPoint(BaseModel):
    id: int
    address: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
