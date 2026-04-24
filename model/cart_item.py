from app import db
from model.product import Product


class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)

    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    quantity = db.Column(db.Integer, default=1)

    price = db.Column(db.Float, nullable=False)

    # ✅ THIS FIXES YOUR ERROR
    product = db.relationship('Product', foreign_keys=[product_id])