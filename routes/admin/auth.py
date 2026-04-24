from flask import url_for,flash,session
from werkzeug.security import check_password_hash
from werkzeug.utils import redirect

from model.user import User
from app import app, render_template, request

@app.get('/login')
def login():
    return render_template('admin/Auth/login.html')

@app.post('/do_login')
def do_login():
    session.clear()
    form = request.form
    username = form.get('username')
    password = form.get('password')
    user = User.query.filter_by(username=username).first()
    if user:
        if check_password_hash(user.password, password):
            session.clear()
            session['user_id'] = user.id
            session['username'] = user.username
            session['profile'] = user.profile
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboards'))
        else:
            flash('invalid password or username')
            return redirect(url_for('login'))
    flash("invalid password or username")
    return redirect(url_for('login'))


@app.get('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))