from flask_sqlalchemy import SQLAlchemy
from models.base import BaseModel

db = SQLAlchemy()

class Article(BaseModel):
    __tablename__ = 'articles'

    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    author = db.relationship("User", backref="articles")
