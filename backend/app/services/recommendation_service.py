from app.models.product import Product


def recommend_product(db, budget, category):
    products = (
        db.query(Product)
        .filter(
            Product.category.ilike(category),
            Product.price <= budget
        )
        .order_by(Product.rating.desc())
        .all()
    )

    if not products:
        return None

    return products[0]