from app import app, render_template
import requests

@app.get('/admin/order')
def orders():
    module = 'order'
    return render_template('admin/Order/index.html',module=module)
