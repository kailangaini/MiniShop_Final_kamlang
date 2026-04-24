import os
from app import app, db
from flask import request, redirect, render_template, url_for, abort
from sqlalchemy import text
from model.category import getAllCategories
from model.product import Product, getProductById, getAllProductlist
from upload_service import save_image


# ---------------------------
# LIST PRODUCTS
# ---------------------------
@app.get('/admin/product')
def products():
    module = 'product'
    rows = getAllProductlist()
    return render_template(
        'admin/Product/index.html',
        module=module,
        products=rows
    )


# ---------------------------
# PRODUCT FORM
# ---------------------------
@app.get('/admin/product/form')
def form_product():
    module = 'product'
    action = request.args.get('action', 'add')

    if action not in ['add', 'edit']:
        return abort(404)

    pro_id = request.args.get('pro_id', 0)
    status = 'add' if action == 'add' else 'edit'

    product = None
    if status == 'edit':
        product = getProductById(pro_id)

    return render_template(
        'admin/Product/form.html',
        module=module,
        status=status,
        pro_id=pro_id,
        product=product,
        category=getAllCategories()
    )


# ---------------------------
# CONFIRM DELETE
# ---------------------------
@app.get('/admin/product/confirm')
def confirm_product():
    module = 'product'
    pro_id = int(request.args.get('pro_id'))

    product = Product.query.get(pro_id)
    if not product:
        return 'no product found!'

    return render_template(
        'admin/Product/confirm.html',
        module=module,
        product=product
    )


# ---------------------------
# DELETE PRODUCT
# ---------------------------
@app.post('/admin/product/delete')
def delete_product():
    pro_id = int(request.form.get('pro_id'))
    delete_image = request.form.get('delete_image')

    product = Product.query.get(pro_id)
    if not product:
        return 'no product found!'

    # delete images
    for fname in [
        delete_image,
        f"resized_{delete_image}",
        f"thumb_{delete_image}"
    ]:
        path = os.path.join(app.config['UPLOAD_FOLDER'], fname)
        if os.path.isfile(path):
            os.remove(path)

    db.session.delete(product)
    db.session.commit()

    return redirect(url_for('products'))


# ---------------------------
# ADD PRODUCT (with qty)
# ---------------------------
@app.post('/admin/product/add')
def add_product():
    file = request.files.get('image')
    filename = None

    if file:
        images = save_image(
            file,
            app.config['UPLOAD_FOLDER'],
            app.config['ALLOWED_EXTENSIONS']
        )
        filename = images['original']

    product = Product(
        name=request.form.get('name'),
        category_id=request.form.get('category'),
        cost=request.form.get('cost'),
        price=request.form.get('price'),
        qty=request.form.get('qty'),   # ✅ STOCK
        description=request.form.get('description'),
        image=filename
    )

    db.session.add(product)
    db.session.commit()

    return redirect(url_for('products'))


# ---------------------------
# EDIT PRODUCT (with qty)
# ---------------------------
@app.post('/admin/product/edit')
def edit_product():
    product_id = request.form.get('product_id')

    product = Product.query.get(product_id)
    if not product:
        return 'no product found!'

    product.name = request.form.get('name')
    product.category_id = request.form.get('category')
    product.cost = request.form.get('cost')
    product.price = request.form.get('price')
    product.qty = request.form.get('qty')   # ✅ STOCK UPDATE
    product.description = request.form.get('description')

    file = request.files.get('image')
    old_image = request.form.get('old_image')

    if file and file.filename != '':
        images = save_image(
            file,
            app.config['UPLOAD_FOLDER'],
            app.config['ALLOWED_EXTENSIONS']
        )

        product.image = images['original']

        # delete old images
        for fname in [
            old_image,
            f"resized_{old_image}",
            f"thumb_{old_image}"
        ]:
            path = os.path.join(app.config['UPLOAD_FOLDER'], fname)
            if os.path.isfile(path):
                os.remove(path)
    else:
        product.image = old_image

    db.session.commit()

    return redirect(url_for('products'))