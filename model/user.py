from app import db
from sqlalchemy import text

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    profile =db.Column(db.String(128),)


def getAllUsers():
    sql = text("""
                   SELECT * from user
            """)
    result = db.session.execute(sql)
    rows = [dict(row._mapping) for row in result]
    return rows
