from app import app, db
from flask import request, redirect, render_template, url_for, abort
from model.category import Category, getAllCategories


# List all categories
@app.get('/admin/category')
def categorys():
    module = 'category'
    rows = getAllCategories()
    return render_template(
        'admin/category/index.html',
        module=module,
        categories=rows
    )


# Category form (add/edit)
@app.get('/admin/category/form')
def form_category():
    module = 'category'
    action = request.args.get('action', 'add')
    if action not in ['add', 'edit']:
        return abort(404)

    cat_id = request.args.get('cat_id', 0)
    status = 'add' if action == 'add' else 'edit'
    category = None
    if status == 'edit':
        category = Category.query.get(cat_id)
        if not category:
            return 'Category not found!'

    return render_template(
        'admin/category/form.html',
        module=module,
        status=status,
        cat_id=cat_id,
        category=category
    )


# Confirm delete category
@app.get('/admin/category/confirm')
def confirm_category():
    module = 'category'
    cat_id = int(request.args.get('cat_id'))
    category = Category.query.get(cat_id)
    if not category:
        return 'No category found!'
    return render_template(
        'admin/category/confirm.html',
        module=module,
        category=category
    )


# Delete category
@app.post('/admin/category/delete')
def delete_category():
    cat_id = int(request.form.get('cat_id'))
    category = Category.query.get(cat_id)
    if not category:
        return 'No category found!'

    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('categorys'))


# Add category
@app.post('/admin/category/add')
def add_category():
    name = request.form.get('name')

    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    return redirect(url_for('categorys'))


# Edit category
@app.post('/admin/category/edit')
def edit_category():
    cat_id = request.form.get('category_id')
    name = request.form.get('name')

    category = Category.query.get(cat_id)
    if not category:
        return 'No category found!'

    category.name = name
    db.session.commit()
    return redirect(url_for('categorys'))
