from flask import render_template, session, request, redirect, url_for
from app import app
from model.cart import Cart


def get_cart():
    user_id = session.get('user_id')
    cart = None

    if user_id:
        cart = Cart.query.filter_by(user_id=user_id).first()
    else:
        cart_id = session.get('cart_id')
        if cart_id:
            cart = Cart.query.get(cart_id)

    return cart


def get_total():
    cart = get_cart()

    if cart and cart.items:
        return sum(float(i.price) * i.quantity for i in cart.items)

    return 0


@app.route('/payment', methods=['GET', 'POST'])
def payment():

    cart = get_cart()

    if not cart:
        return redirect('/cart')

    items = cart.items or []

    total = sum(float(i.price) * i.quantity for i in items)

    if total <= 0:
        return redirect('/cart')

    if request.method == 'POST':

        customer_name = request.form.get("customer_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        address = request.form.get("address")

        if not all([customer_name, email, phone, address]):
            return render_template(
                'pageFront/payment.html',
                cart_total=total,
                cart=cart,
                error="Please fill all fields"
            )

        session['checkout'] = {
            "customer_name": customer_name,
            "email": email,
            "phone": phone,
            "address": address
        }

        return redirect(url_for('qr_payment'))

    return render_template(
        'pageFront/payment.html',
        cart_total=total,
        cart=cart
    )