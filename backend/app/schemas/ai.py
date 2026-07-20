from pydantic import BaseModel

class AIRequest(BaseModel):
    query: str

class CompareRequest(BaseModel):
    product1: str
    product2: str