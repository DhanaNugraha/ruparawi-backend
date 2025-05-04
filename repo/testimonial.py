from models.testimonial import VendorTestimonial
from instance.database import db

def create_testimonial(vendor_id, message):
    testimonial = VendorTestimonial(
        vendor_id=vendor_id,
        message=message
    )
    db.session.add(testimonial)
    db.session.commit()
    return testimonial

def get_all_testimonials():
    return VendorTestimonial.query.all()

def get_testimonial_by_id(testimonial_id):
    return VendorTestimonial.query.get(testimonial_id)

def update_testimonial(testimonial_id, message):
    testimonial = VendorTestimonial.query.get(testimonial_id)
    if testimonial:
        testimonial.message = message
        db.session.commit()
    return testimonial

def delete_testimonial(testimonial_id):
    testimonial = VendorTestimonial.query.get(testimonial_id)
    if testimonial:
        db.session.delete(testimonial)
        db.session.commit()
    return testimonial