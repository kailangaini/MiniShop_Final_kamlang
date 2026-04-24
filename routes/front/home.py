from app import app,session
from flask import render_template, request
from model.product import getAllProductlist
from model.category import getAllCategories

def normalize_products(products):
    data = []
    for p in products:
        image_url = None
        if p.get("image"):
            image_url = f"/static/uploads/{p['image']}"

        data.append({
            "id": p["id"],
            "name": p["name"],
            "price": p["price"],
            "qty": p.get("qty", 0),   # ✅ ADD THIS
            "description": p.get("description"),
            "image": image_url,
            "category": p.get("category")
        })
    return data
@app.get('/')
@app.get('/home',endpoint='home')
def home():
    products = getAllProductlist()
    categories = getAllCategories()

    products = normalize_products(products)

    return render_template(
        'pageFront/home.html',
        products=products,
        categories=categories,
        selected_category=None
    )

@app.get("/products",endpoint="products_filter")
def products_filter():
    category = request.args.get('category')
    products = getAllProductlist()
    categories = getAllCategories()

    products = normalize_products(products)

    if category:
        products = [p for p in products if p['category'] == category]

    return render_template(
        'pageFront/home.html',
        products=products,
        categories=categories,
        selected_category=category
    )

