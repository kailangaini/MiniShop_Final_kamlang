from flask import jsonify, render_template, request, session
from app import app, db
from model.product import Product
from model.cart import Cart
from model.cart_item import CartItem


# =========================
# GET CART (GUEST ONLY)
# =========================
@app.get('/cart')
def cart():

    cart_id = session.get('cart_id')

    cart = None

    if cart_id:
        cart = Cart.query.filter_by(id=cart_id, status=0).first()

    if not cart:
        return render_template('pageFront/cart.html', items=[], total=0)

    items = cart.items

    cart_data = []
    total = 0

    for i in items:
        subtotal = i.price * i.quantity
        total += subtotal

        product = i.product

        cart_data.append({
            "id": i.id,
            "price": i.price,
            "quantity": i.quantity,
            "stock": product.qty,
            "product": {
                "id": product.id,
                "name": product.name,
                "image": product.image
            }
        })

    return render_template(
        'pageFront/cart.html',
        items=cart_data,
        total=total
    )


# =========================
# ADD TO CART
# =========================
@app.post('/cart/add')
def add_to_cart():

    data = request.get_json()

    product_id = int(data.get('product_id'))
    qty = int(data.get('qty', 1))

    product = Product.query.get(product_id)

    if not product:
        return jsonify({"success": False}), 404

    cart_id = session.get('cart_id')
    cart = None

    if cart_id:
        cart = Cart.query.filter_by(id=cart_id, status=0).first()

    if not cart:
        cart = Cart(status=0)
        db.session.add(cart)
        db.session.commit()
        session['cart_id'] = cart.id

    item = CartItem.query.filter_by(
        cart_id=cart.id,
        product_id=product_id
    ).first()

    if item:
        item.quantity += qty
    else:
        db.session.add(CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=qty,
            price=product.price
        ))

    db.session.commit()

    return jsonify({"success": True})


# =========================
# UPDATE CART
# =========================
@app.post('/cart/update')
def update_cart_item():

    item = CartItem.query.get(request.json.get('item_id'))
    qty = int(request.json.get('qty', 1))

    if not item:
        return {"status": "error"}, 404

    product = Product.query.get(item.product_id)

    if qty > product.qty:
        qty = product.qty

    if qty <= 0:
        db.session.delete(item)
    else:
        item.quantity = qty

    db.session.commit()

    return {"status": "success"}


# =========================
# REMOVE ITEM
# =========================
@app.post('/cart/remove')
def remove_cart_item():

    item = CartItem.query.get(request.json.get('item_id'))

    if item:
        db.session.delete(item)
        db.session.commit()

    return {"status": "success"}