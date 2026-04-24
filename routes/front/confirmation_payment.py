from app import app, render_template
from flask import session, redirect
from model import Order, OrderItem, Product


@app.get('/confirmation_payment')
def confirmation_payment():

    order_id = session.get("order_id")

    if not order_id:
        return redirect('/')

    order = Order.query.get(order_id)

    if not order:
        return redirect('/')

    items = OrderItem.query.filter_by(order_id=order.id).all()

    # 🔥 ENRICH ITEMS WITH PRODUCT DATA
    items_data = []

    for i in items:
        product = Product.query.get(i.product_id)

        items_data.append({
            "name": product.name if product else "Unknown",
            "quantity": i.quantity,
            "price": i.price
        })

    invoice = f"INV{order.id}"

    session.pop("order_id", None)
    session.pop("cart_id", None)
    session.pop("checkout", None)

    return render_template(
        'pageFront/confirmation_payment.html',
        order=order,
        items=items_data,
        invoice=invoice
    )