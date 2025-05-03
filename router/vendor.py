from flask import Blueprint, request
from flask_jwt_extended import current_user, jwt_required
from auth.auth import vendor_required
from views.vendor import get_vendor_products_view, get_vendor_profile_view, get_vendor_recent_orders_view, get_vendor_stats_view, update_vendor_profile_view, vendor_register_view

vendor_router = Blueprint("vendor_router", __name__, url_prefix="/vendor")


@vendor_router.route("/apply", methods=["POST"])
@jwt_required()
def apply_as_vendor():
    return vendor_register_view(current_user, request.json)


@vendor_router.route("/profile", methods=["GET", "PUT"])
@jwt_required()
def vendor_profile():
    match request.method.lower():
        case "get":
            return get_vendor_profile_view(current_user)
        case "put":
            return update_vendor_profile_view(current_user, request.json)


@vendor_router.route("/products", methods=["GET"])
@jwt_required()
@vendor_required
def get_vendor_products():
    return get_vendor_products_view(current_user)


@vendor_router.route("/stats", methods=["GET"])
@jwt_required()
@vendor_required
def get_vendor_stats():
    return get_vendor_stats_view(current_user)


@vendor_router.route("/recent-orders", methods=["GET"])
@jwt_required()
@vendor_required
def get_vendor_recent_orders():
    return get_vendor_recent_orders_view(current_user)