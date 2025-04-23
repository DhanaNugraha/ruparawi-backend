from flask import Blueprint, request
from flask_jwt_extended import current_user, jwt_required

from views.user import get_public_user_profile_view, update_user_profile_view

user_router = Blueprint("user_router", __name__, url_prefix="/user")

@user_router.route("/<int:user_id>", methods=["GET"])
def get_public_profile(user_id):
    return get_public_user_profile_view(user_id)

# private path
@user_router.route("/me", methods=["PUT"])
@jwt_required()
def update_profile():
    return update_user_profile_view(current_user, request.json)