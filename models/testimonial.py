from instance.database import db
from models.base import BaseModel

class VendorTestimonial(db.Model, BaseModel):
    __tablename__ = 'vendor_testimonials'
    
    vendor_id = db.Column(db.Integer, db.ForeignKey("vendor_profiles.user_id"), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey("admin_users.user_id"), nullable=False)
    message = db.Column(db.Text, nullable=False)

    # Relationships
    vendor = db.relationship("VendorProfile", backref=db.backref("testimonials", lazy=True))
    admin = db.relationship("AdminUser", backref=db.backref("testimonials", lazy=True))