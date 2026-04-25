from app import app, render_template
from model.order import Order
from sqlalchemy.orm import joinedload

@app.get('/admin/order')
def orders():
    orders = Order.query.options(
        joinedload(Order.items)
    ).order_by(Order.id.desc()).all()

    return render_template(
        'admin/Order/index.html',
        orders=orders
    )