import os
from app import app, db
from flask import request, redirect, render_template, url_for, abort
from model.user import User,getAllUsers
from upload_service import save_image
from werkzeug.security import generate_password_hash, check_password_hash

@app.get('/admin/user')
def users():
    rows = getAllUsers()
    return render_template('admin/User/index.html', users=rows)

@app.get('/admin/user/form')
def form_user():
    action = request.args.get('action', 'add')
    if action not in ['add', 'edit']:
        return abort(404)

    user_id = request.args.get('user_id', 0)
    status = 'add' if action=='add' else 'edit'
    user = None
    if status=='edit':
        user = User.query.get(user_id)

    return render_template(
        'admin/User/form.html',
        status=status,
        user=user
    )

@app.get('/admin/user/confirm')
def confirm_user():
    user_id = int(request.args.get('user_id'))
    user = User.query.get(user_id)
    if not user:
        return 'No user found!'
    return render_template('admin/User/confirm.html', user=user)

@app.post('/admin/user/delete')
def delete_user():
    user_id = int(request.form.get('user_id'))
    delete_profile = request.form.get('delete_profile')
    user = User.query.get(user_id)

    if delete_profile:
        for fname in [delete_profile, f"resized_{delete_profile}", f"thumb_{delete_profile}"]:
            path = os.path.join(app.config['UPLOAD_FOLDER'], fname)
            if os.path.isfile(path):
                os.remove(path)

    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('users'))

@app.post('/admin/user/add')
def add_user():
    file = request.files.get('profile')
    filename = None
    if file:
        images = save_image(file, app.config['UPLOAD_FOLDER'], app.config['ALLOWED_EXTENSIONS'])
        filename = images['original']

    username = request.form.get('username')
    password = request.form.get('password')

    user = User(username=username,
                password=generate_password_hash(password),
                profile=filename
    )
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('users'))

@app.post('/admin/user/edit')
def edit_user():
    user_id = request.form.get('user_id')
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.get(user_id)
    if not user:
        return 'No user found!'

    user.username = username
    if password:
        user.password = password

    file = request.files.get('profile')
    old_profile = request.form.get('old_profile')

    if file and file.filename != '':
        images = save_image(file, app.config['UPLOAD_FOLDER'], app.config['ALLOWED_EXTENSIONS'])
        user.profile = images['original']
        for fname in [old_profile, f"resized_{old_profile}", f"thumb_{old_profile}"]:
            path = os.path.join(app.config['UPLOAD_FOLDER'], fname)
            if os.path.isfile(path):
                os.remove(path)
    else:
        user.profile = old_profile

    db.session.commit()
    return redirect(url_for('users'))
