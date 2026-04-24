import os
import qrcode
from flask import render_template, session, redirect, request, jsonify
from app import app, db
from model import Order, OrderItem, Product
from model.cart import Cart
from bakong_khqr import KHQR


token_string = os.getenv("KHQR_TOKEN")


# =========================
# HELPERS
# =========================
def get_cart():
    cart_id = session.get('cart_id')
    if cart_id:
        return Cart.query.filter_by(id=cart_id, status=0).first()
    return None


def get_total(cart):
    if cart and cart.items:
        return sum(i.price * i.quantity for i in cart.items)
    return 0


# =========================
# QR PAYMENT
# =========================
@app.route('/qr-payment')
def qr_payment():

    checkout = session.get("checkout")
    if not checkout:
        return redirect('/payment')

    cart = get_cart()
    if not cart or not cart.items:
        return redirect('/cart')

    total = get_total(cart)

    # CREATE ORDER
    order = Order(
        customer_name=checkout["customer_name"],
        email=checkout["email"],
        phone=checkout["phone"],
        address=checkout["address"],
        total=total,
        payment_status="Pending",
        status="Pending"
    )

    db.session.add(order)
    db.session.commit()

    session["order_id"] = order.id

    # ORDER ITEMS
    for item in cart.items:
        db.session.add(OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price
        ))

    db.session.commit()

    invoice = f"INV{order.id}"

    khqr = KHQR(token_string)

    qr = khqr.create_qr(
        bank_account='yin_kamlang@bkrt',
        merchant_name='KaiShop',
        merchant_city='Phnom Penh',
        amount=float(total),
        currency='KHR',
        bill_number=invoice,
        static=False,
        expiration=1
    )

    os.makedirs("static/qrcodes", exist_ok=True)

    filename = f"{invoice}.png"
    qrcode.make(qr).save(f"static/qrcodes/{filename}")

    return render_template(
        'pageFront/qr_payment.html',
        qr=qr,
        filename=filename,
        order=order,
        invoice=invoice,
        cart_total=total
    )


# =========================
# CHECK PAYMENT
# =========================
@app.get('/check_status')
def check_status():

    try:
        qr = request.args.get('qrcode')
        if not qr:
            return jsonify({"status": "ERROR", "message": "missing qrcode"}), 400

        khqr = KHQR(token_string)

        md5 = khqr.generate_md5(qr)
        result = khqr.check_payment(md5)

        status = None

        if isinstance(result, dict):
            status = result.get("data", {}).get("status")
        elif isinstance(result, str):
            status = result

        status = str(status).strip().upper() if status else "PENDING"

        print("STATUS:", status)

        # =========================
        # PAYMENT SUCCESS
        # =========================
        if status == "PAID":

            order_id = session.get("order_id")
            cart_id = session.get("cart_id")

            order = Order.query.get(order_id)
            cart = Cart.query.filter_by(id=cart_id).first()

            if order:
                order.payment_status = "Paid"
                order.status = "Confirmed"
                # deduct stock
                for item in order.items:
                    product = Product.query.get(item.product_id)
                    if product:
                        product.qty -= item.quantity

            if cart:
                cart.status = 1

            db.session.commit()

            return jsonify({"status": "PAID"})

        # not paid
        return jsonify({"status": status})

    except Exception as e:
        print("CHECK_STATUS ERROR:", e)
        return jsonify({"status": "ERROR"}), 500