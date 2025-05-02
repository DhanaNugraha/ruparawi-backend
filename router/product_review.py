from flask import Blueprint, request, jsonify
from repo import product_review as review_repo

product_review_router = Blueprint("product_review", __name__, url_prefix="/review")

@product_review_router.route("/", methods=["POST"])
def create_product_review():
    data = request.json
    review = review_repo.create_review(
        product_id=data["product_id"],
        user_id=data["user_id"],
        rating=data["rating"],
        comment=data.get("comment")
    )
    return jsonify({
        "id": review.id,
        "product_id": review.product_id,
        "user_id": review.user_id,
        "rating": review.rating,
        "comment": review.comment
    }), 201

@product_review_router.route("/product/<int:product_id>", methods=["GET"])
def get_reviews_for_product(product_id):
    reviews = review_repo.get_reviews_by_product(product_id)
    return jsonify([
        {
            "id": r.id,
            "product_id": r.product_id,
            "user_id": r.user_id,
            "rating": r.rating,
            "comment": r.comment
        } for r in reviews
    ])

@product_review_router.route("/<int:review_id>", methods=["GET"])
def get_review_detail(review_id):
    review = review_repo.get_review_by_id(review_id)
    if not review:
        return jsonify({"error": "Review not found"}), 404
    return jsonify({
        "id": review.id,
        "product_id": review.product_id,
        "user_id": review.user_id,
        "rating": review.rating,
        "comment": review.comment
    })

@product_review_router.route("/<int:review_id>/edit", methods=["PUT"])
def edit_review_by_id(review_id):
    data = request.json
    updated = review_repo.update_review(
        review_id,
        rating=data.get("rating"),
        comment=data.get("comment")
    )
    if not updated:
        return jsonify({"error": "Review not found"}), 404
    return jsonify({
        "id": updated.id,
        "product_id": updated.product_id,
        "user_id": updated.user_id,
        "rating": updated.rating,
        "comment": updated.comment
    })

@product_review_router.route("/<int:review_id>/delete", methods=["DELETE"])
def remove_review_by_id(review_id):
    deleted = review_repo.delete_review(review_id)
    if not deleted:
        return jsonify({"error": "Review not found"}), 404
    return jsonify({"message": "Review deleted successfully"})
