from flask import redirect, url_for

from app import app, render_template, request
import requests

BOT_TOKEN = "8453489234:AAHp9hSZNZtAFk5JnKLLh5jMpRD-z4zg8hw"
CHAT_ID = "@kamlangTestbot"

@app.get('/contact')
def contact():
    status = request.args.get('status')
    return render_template('pageFront/contact.html', status=status)

@app.post('/contact')
def contact_submit():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    phone = request.form.get('phone')

    text = f"📩 New Contact Message:\n\nName: {name}\nEmail: {email}\nPhone Number: {phone}\nMessage: {message}"

    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': text}
    response = requests.post(url, data=data)

    if response.ok:
        status = 'Your message has been sent successfully!'
    else:
        status = f'Failed to send message: {response.text}'

    return redirect(url_for('contact', status=status))
