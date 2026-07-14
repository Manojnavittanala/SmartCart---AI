import csv

from app.database.database import SessionLocal
from app.models.product import Product

db = SessionLocal()

with open("products.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:

        product = Product(
            name=row["name"],
            brand=row["brand"],
            category=row["category"],
            description=row["description"],
            price=float(row["price"]),
            rating=float(row["rating"]),
            stock=int(row["stock"]),
            image=row["image"]
        )

        db.add(product)

db.commit()
db.close()

print("✅ Products imported successfully!")