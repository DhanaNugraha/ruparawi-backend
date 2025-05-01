from instance.database import db
from .base import BaseModel
from shared import time

class ProductReview(db.Model, BaseModel):
    __tablename__ = 'product_reviews'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1–5
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=time.now)

    def __repr__(self):
        return f"<Review {self.id} for Product {self.product_id}>"
