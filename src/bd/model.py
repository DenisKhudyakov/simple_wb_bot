from sqlalchemy import Column, Integer, String

from src.config import Base


class Product(Base):
    """Модель товара"""
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    price = Column(Integer, nullable=False)
    cashback = Column(Integer, nullable=False)
    url = Column(String(250), nullable=False)
    sub_category = Column(String(250), nullable=False)
