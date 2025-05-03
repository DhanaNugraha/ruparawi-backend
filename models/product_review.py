from instance.database import db
from .base import BaseModel

class ProductReview(db.Model, BaseModel):
    __tablename__ = 'product_reviews'

    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1–5
    comment = db.Column(db.Text, nullable=True)
    
     # Relationships
    product = db.relationship('Product', backref=db.backref('reviews', lazy=True))
    user = db.relationship('User', backref=db.backref('reviews', lazy=True))

    def __repr__(self):
        return f"<Review {self.id} for Product {self.product_id}>"
