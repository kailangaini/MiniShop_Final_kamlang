from app import app, render_template
import requests

@app.get('/admin/customer')
def customers():
    module = 'customer'
    return render_template('admin/Order/index.html',module=module)
