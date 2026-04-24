from app import db
from datetime import datetime


class Cart(db.Model):
    __tablename__ = 'carts'

    id = db.Column(db.Integer, primary_key=True)

    # optional: guest or logged-in user
    user_id = db.Column(db.Integer, nullable=True)

    #  ADD THIS (IMPORTANT)
    status = db.Column(db.Integer, default=0)
    # 0 = active cart
    # 1 = completed (paid)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship(
        'CartItem',
        backref='cart',
        cascade="all, delete-orphan",
        lazy=True
    )