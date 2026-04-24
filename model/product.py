from app import db
from sqlalchemy import text


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(128), unique=True, nullable=False)

    category_id = db.Column(
        db.Integer,
        db.ForeignKey('category.id'),
        nullable=False
    )

    cost = db.Column(db.Float, nullable=False)

    price = db.Column(db.Float, nullable=False)

    qty = db.Column(db.Integer, default=0, nullable=False)

    image = db.Column(db.String(128))

    description = db.Column(db.String(128))


# -------------------------
# GET ALL PRODUCTS
# -------------------------
def getAllProductlist():
    sql = text("""
        SELECT 
            p.id,
            p.name,
            c.name as category,
            p.cost,
            p.price,
            p.qty,
            p.image,
            p.description
        FROM product p
        INNER JOIN category c
            ON p.category_id = c.id;
    """)
    result = db.session.execute(sql)
    return [dict(row._mapping) for row in result]


# -------------------------
# GET PRODUCT BY ID
# -------------------------
def getProductById(product_id: int):
    sql = text("""
        SELECT 
            p.id,
            p.name,
            c.name as category,
            p.cost,
            p.price,
            p.qty,
            p.image,
            p.description
        FROM product p
        INNER JOIN category c
            ON p.category_id = c.id
        WHERE p.id = :product_id;
    """)

    result = db.session.execute(
        sql,
        {'product_id': int(product_id)}
    ).fetchone()

    if result:
        return dict(result._mapping)

    return {"error": "Product not found"}