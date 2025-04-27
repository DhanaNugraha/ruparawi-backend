from flask import Blueprint, request
from flask_jwt_extended import current_user, jwt_required
from views.vendor import vendor_register_view

vendor_router = Blueprint("vendor_router", __name__, url_prefix="/vendor")


@vendor_router.route("/apply", methods=["POST"])
@jwt_required()
def apply_as_vendor():
    return vendor_register_view(current_user, request.json)
