from werkzeug.security import generate_password_hash
from app import app, db
from model.user import User

with app.app_context():
    admin = User(
        username="admin",
        password=generate_password_hash("123123"),
    )

    db.session.add(admin)
    db.session.commit()
    print("Admin seeded successfully")
