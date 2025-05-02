from flask import render_template
from repo import product_review

def render_product_reviews_page(product_id):
    reviews = product_review.get_reviews_by_product(product_id)
    return render_template("product_reviews.html", reviews=reviews)
