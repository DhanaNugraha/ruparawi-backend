from flask import Blueprint, request
from flask_jwt_extended import current_user, jwt_required
from views.auth import get_user_view, refresh_token_view, user_login_view, user_register_view

auth_router = Blueprint("auth_router", __name__, url_prefix="/auth")


@auth_router.route("/register", methods=["POST"])
def user_register():
    return user_register_view(request.json)


@auth_router.route("/login", methods=["POST"])
def login():
    return user_login_view(request.json)


@auth_router.route("/me", methods=["GET"])
@jwt_required()  # Requires login to get valid JWT token
def get_current_user():
    return get_user_view(current_user)

@auth_router.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    return refresh_token_view(current_user)


