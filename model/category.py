from app import db
from sqlalchemy import text


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)


def getAllCategories():
    sql = text("""
        SELECT * FROM category
    """)
    result = db.session.execute(sql)
    rows = [dict(row._mapping) for row in result]
    return rows