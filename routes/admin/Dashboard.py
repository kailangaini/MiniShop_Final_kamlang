from app import app
from flask import render_template,redirect,request,flash,session,url_for

@app.get('/admin')
@app.get('/admin/dashboard')
def dashboards():
    module = 'dashboard'
    return render_template('admin/Dashboard/index.html',module=module)
