from instance.database import db
from models.base import BaseModel
from shared import time

class VendorTestimonial(db.Model, BaseModel):
    __tablename__ = 'vendor_testimonials'
    
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey("vendor_profiles.user_id"), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey("admin_users.user_id"), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=time.now)

    # Relationships
    vendor = db.relationship("VendorProfile", back_populates="testimonials")
    admin = db.relationship("AdminUser", back_populates="received_testimonials")