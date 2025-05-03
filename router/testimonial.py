from flask import Blueprint, request, jsonify
from repo import testimonial as testimonial_repo
from views.testimonial import render_testimonial_page

testimonial_router = Blueprint("testimonial", __name__, url_prefix="/testimonial")

@testimonial_router.route("/", methods=["POST"])
def create_testimonial():
    data = request.json
    testimonial = testimonial_repo.create_testimonial(
        vendor_id=data["vendor_id"],
        admin_id=data["admin_id"],
        message=data["message"]
    )
    return jsonify({
        "id": testimonial.id,
        "vendor_id": testimonial.vendor_id,
        "admin_id": testimonial.admin_id,
        "message": testimonial.message
    }), 201

@testimonial_router.route("/", methods=["GET"])
def get_all():
    testimonials = testimonial_repo.get_all_testimonials()
    return jsonify([
        {
            "id": t.id,
            "vendor_id": t.vendor_id,
            "admin_id": t.admin_id,
            "message": t.message
        } for t in testimonials
    ])

@testimonial_router.route("/<int:testimonial_id>", methods=["PUT"])
def update(testimonial_id):
    data = request.json
    updated = testimonial_repo.update_testimonial(testimonial_id, data["message"])
    if not updated:
        return jsonify({"error": "Testimonial Not found"}), 404
    return jsonify({"id": updated.id, "message": updated.message})

@testimonial_router.route("/<int:testimonial_id>", methods=["DELETE"])
def delete(testimonial_id):
    deleted = testimonial_repo.delete_testimonial(testimonial_id)
    if not deleted:
        return jsonify({"error": "Testimonial Not found"}), 404
    return jsonify({"message": "Testimonial deleted successfully"})

@testimonial_router.route("/web", methods=["GET"])
def testimonial_web_view():
    return render_testimonial_page()