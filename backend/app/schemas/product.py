from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    brand: str
    category: str
    description: str
    price: float
    rating: float
    stock: int
    image: str


class ProductResponse(ProductCreate):
    id: int

    class Config:
        from_attributes = True