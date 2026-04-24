from flask import render_template, abort
from app import app
from model.product import Product

@app.get('/product_details/<int:product_id>')
def product_details(product_id):
    # Fetch product from database
    product = Product.query.get(product_id)
    if not product:
        abort(404)

    # Prepare images for carousel
    images = []
    if product.image:
        images.append(f"/static/uploads/{product.image}")
    if getattr(product, 'resized_image', None):
        images.append(f"/static/uploads/{product.resized_image}")
    if getattr(product, 'thumbnail_image', None):
        images.append(f"/static/uploads/{product.thumbnail_image}")

    # Prepare data for template
    product_data = {
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "description": product.description,
        "image": images[0] if images else None,
        "images": images
    }

    return render_template('pageFront/product_details.html', product=product_data)
