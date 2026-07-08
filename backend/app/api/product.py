from fastapi import APIRouter

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("/")
def get_products():
    return {
        "message": "List of Products"
    }


@router.post("/")
def add_product():
    return {
        "message": "Product Added Successfully"
    }