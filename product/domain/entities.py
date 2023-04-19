from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, Float, DateTime

from shared.db_orm import Base
from shared.ddd import AggregateRoot


class Product(Base, AggregateRoot):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    dish_id = Column(Integer, nullable=False)
    name = Column(String)
    description = Column(Text)
    price = Column(Float)
    calories_per_100g = Column(Float)
    calories_per_serving = Column(Float)
    ingredients = Column(Text)
    weight = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
