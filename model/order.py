from app import db
from datetime import datetime


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, nullable=True)

    # ✅ NEW (checkout fields)
    customer_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(255), nullable=False)

    total = db.Column(db.Float, nullable=False)

    # ✅ KHQR support
    payment_method = db.Column(db.String(50), default='KHQR')
    payment_status = db.Column(db.String(50), default='Pending')

    status = db.Column(db.String(50), default='Pending')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship(
        'OrderItem',
        backref='order',
        cascade="all, delete-orphan"
    )