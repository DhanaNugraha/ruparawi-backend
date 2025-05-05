from instance.database import db
from models.base import BaseModel

class Article(db.Model, BaseModel):
    __tablename__ = 'articles'

    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    author = db.relationship("User", backref="articles")
