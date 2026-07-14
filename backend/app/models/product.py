from sqlalchemy import Column, Integer, String, Float
from app.database.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)

    category = Column(String)

    description = Column(String)

    price = Column(Float)

    rating = Column(Float, default=0)

    stock = Column(Integer, default=0)

    image = Column(String)