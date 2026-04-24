import requests
from flask import Flask, render_template, abort, request,redirect,url_for,flash,session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import config
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=12)


app.config.from_object(config)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

import routes

@app.before_request
def before_request():
    url = request.path
    print("REQUEST PATH:", request.path)
    if url.startswith('/admin'):
        if not session.get("user_id"):
            flash("Please log in first.", "warning")
            return redirect(url_for("login", next=request.path))

if __name__ == "__main__":
    app.run()
