from flask import Blueprint, request
from flask_jwt_extended import current_user, jwt_required
from auth.auth import admin_required
from repo.admin import log_admin_action_repo
from views.admin import (
    create_article_view,
    create_category_view,
    create_promotion_view,
    delete_article_view,
    get_all_promotions_view,
    soft_delete_category_view,
    update_article_view,
    update_category_view,
    get_admin_logs_view,
    get_vendors_view,
    review_vendor_application_view,
    update_promotion_view,
)


admin_router = Blueprint("admin_router", __name__, url_prefix="/admin")


@admin_router.route("/category", methods=["POST"])
@jwt_required()
@admin_required()
def create_category():
    return create_category_view(request.json)


@admin_router.route("/category/<int:category_id>", methods=["PUT", "DELETE"])
@jwt_required()
@admin_required()
def category_detail(category_id):
    match request.method.lower():
        case "put":
            return update_category_view(request.json, category_id)

        case "delete":
            return soft_delete_category_view(category_id)


@admin_router.route("/vendors", methods=["GET"])
@jwt_required()
@admin_required()
def get_all_vendors():
    return get_vendors_view()


@admin_router.route("/vendor/<int:user_id>/review", methods=["POST"])
@jwt_required()
@admin_required()
def review_vendor_application(user_id):
    return review_vendor_application_view(user_id, request.json)


@admin_router.route("/logs", methods=["GET"])
@jwt_required()
@admin_required()
def get_admin_logs():
    return get_admin_logs_view()


# ------------------------------------------------------ Management Article --------------------------------------------------
@admin_router.route("/article", methods=["POST"])
@jwt_required()
@admin_required()
def create_article():
    return create_article_view(request.get_json())

@admin_router.route("/article/<int:article_id>", methods=["PUT", "DELETE"])
@jwt_required()
@admin_required()
def article_detail(article_id):
    if request.method=="PUT":
        return update_article_view(request.json, article_id)
    elif request.method=="DELETE":
        return delete_article_view(article_id)


# ------------------ Promotions ------------------


@admin_router.route("/promotions", methods=["POST", "GET"])
@jwt_required()
@admin_required()
def admin_promotions():
    match request.method.lower():
        case "post":
            return create_promotion_view(request.json, current_user)
        case "get":
            return get_all_promotions_view()


@admin_router.route("/promotions/<int:promotion_id>", methods=["PUT"])
@jwt_required()
@admin_required()
def update_promotion(promotion_id):
    return update_promotion_view(promotion_id, request.json)


# ------------------ Admin Logs ------------------


# logs admin actions after every request
@admin_router.after_request
@jwt_required()
def log_admin_actions_after_request(response):
    if request.method in ["PUT", "DELETE", "POST"]:
        log_admin_action_repo(current_user, request)

    return response
