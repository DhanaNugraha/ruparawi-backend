from instance.database import db
from .base import BaseModel


class ProductReview(db.Model, BaseModel):
    __tablename__ = "product_reviews"

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    review_text = db.Column(db.Text)
    is_approved = db.Column(db.Boolean, default=False)


class VendorReview(db.Model, BaseModel):
    __tablename__ = "vendor_reviews"

    vendor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    review_text = db.Column(db.Text)


