from flask import jsonify, render_template, request, session
from app import app, db
from model.product import Product
from model.cart import Cart
from model.cart_item import CartItem


# =========================
# CART HELPER
# =========================
def get_or_create_cart():
    cart_id = session.get("cart_id")

    cart = None

    if cart_id:
        cart = Cart.query.filter_by(id=cart_id).first()

        #  if cart is deleted or already checked out → ignore it
        if not cart or cart.status == 1:
            cart = None

    #  ALSO if cart exists but has NO items → treat as new cart
    if cart and len(cart.items) == 0:
        cart = None

    # ✅ create new cart if needed
    if not cart:
        cart = Cart(status=0)
        db.session.add(cart)
        db.session.commit()

        session["cart_id"] = cart.id

    return cart


# =========================
# VIEW CART
# =========================
@app.get('/cart')
def cart():
    cart = get_or_create_cart()

    items = cart.items if cart else []

    cart_data = []
    total = 0

    for i in items:
        product = i.product
        subtotal = i.price * i.quantity
        total += subtotal

        cart_data.append({
            "id": i.id,
            "price": i.price,
            "quantity": i.quantity,
            "stock": product.qty if product else 0,
            "product": {
                "id": product.id if product else None,
                "name": product.name if product else "",
                "image": product.image if product else ""
            }
        })

    return render_template('pageFront/cart.html', items=cart_data, total=total)


# =========================
# ADD TO CART
# =========================
@app.post('/cart/add')
def add_to_cart():

    data = request.get_json(silent=True) or {}

    product_id = data.get('product_id')
    qty = int(data.get('qty') or 1)

    if not product_id:
        return jsonify({"success": False, "message": "missing product_id"}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"success": False}), 404

    cart = get_or_create_cart()

    item = CartItem.query.filter_by(
        cart_id=cart.id,
        product_id=product_id
    ).first()

    if item:
        item.quantity += qty
    else:
        item = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=qty,
            price=product.price
        )
        db.session.add(item)

    db.session.commit()

    return jsonify({"success": True})


# =========================
# UPDATE CART
# =========================
@app.post('/cart/update')
def update_cart_item():

    data = request.get_json(silent=True) or {}

    item_id = data.get('item_id')
    qty = int(data.get('qty') or 1)

    item = CartItem.query.get(item_id)

    if not item:
        return jsonify({"status": "error"}), 404

    product = Product.query.get(item.product_id)

    if product and qty > product.qty:
        qty = product.qty

    if qty <= 0:
        db.session.delete(item)
    else:
        item.quantity = qty

    db.session.commit()

    return jsonify({"status": "success"})


# =========================
# REMOVE ITEM
# =========================
@app.post('/cart/remove')
def remove_cart_item():

    data = request.get_json(silent=True) or {}
    item_id = data.get('item_id')

    item = CartItem.query.get(item_id)

    if item:
        db.session.delete(item)
        db.session.commit()

    return jsonify({"status": "success"})