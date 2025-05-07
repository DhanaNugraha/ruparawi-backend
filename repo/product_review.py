from models.product_review import ProductReview 
from instance.database import db

def create_review(product_id, user_id, rating, comment=None):
    review = ProductReview(
        product_id=product_id,
        user_id=user_id,
        rating=rating,
        comment=comment
    )
    db.session.add(review)
    db.session.commit()
    return review

def get_reviews_by_product(product_id):
    return db.session.execute(db.select(ProductReview).filter_by(product_id=product_id)).scalars().all()

def get_review_by_id(review_id):
    return db.session.execute(db.select(ProductReview).filter_by(id=review_id)).scalar()

def update_review(review_id, rating=None, comment=None):
    review = db.session.execute(db.select(ProductReview).filter_by(id=review_id)).scalar()
    if review:
        if rating is not None:
            review.rating = rating
        if comment is not None:
            review.comment = comment
        db.session.commit()
    return review

def delete_review(review_id):
    review = db.session.execute(db.select(ProductReview).filter_by(id=review_id)).scalar()
    if review:
        db.session.delete(review)
        db.session.commit()
    return review
