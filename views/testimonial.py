from flask import render_template
from repo.testimonial import get_all_testimonials

def render_testimonial_page():
    testimonials = get_all_testimonials()
    return render_template("testimonials.html", testimonials=testimonials)
