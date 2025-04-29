from instance.database import db
from models.base import BaseModel

class Article(db.Model, BaseModel):
    __tablename__ = 'articles'

    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
