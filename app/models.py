from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)  # client, manager, admin

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    article = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100))
    description = Column(Text)
    manufacturer = Column(String(255))
    supplier = Column(String(255))
    price = Column(Numeric(10, 2), nullable=False)
    unit = Column(String(20))
    quantity_in_stock = Column(Integer, nullable=False, default=0)
    discount_percent = Column(Integer, default=0)
    image_path = Column(String(255))

class PickupPoint(Base):
    __tablename__ = "pickup_points"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(255), nullable=False)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    article = Column(String(50), ForeignKey("products.article", ondelete="RESTRICT"), nullable=False)
    status = Column(String(50), nullable=False)
    pickup_point_id = Column(Integer, ForeignKey("pickup_points.id"), nullable=False)
    order_date = Column(Date, nullable=False)
    issue_date = Column(Date, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Связи (опционально, для удобства)
    product = relationship("Product", backref="orders")
    pickup_point = relationship("PickupPoint")
    user = relationship("User")