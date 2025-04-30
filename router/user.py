from flask import Blueprint, request
from flask_jwt_extended import current_user, jwt_required

from views.user import add_address_view, add_payment_method_view, delete_address_view, delete_payment_method_view, get_all_address_view, get_payment_methods_view, get_public_user_profile_view, update_address_view, update_payment_method_view, update_user_profile_view

user_router = Blueprint("user_router", __name__, url_prefix="/user")

@user_router.route("/<int:user_id>", methods=["GET"])
def get_public_profile(user_id):
    return get_public_user_profile_view(user_id)

# private path
@user_router.route("/me", methods=["PUT"])
@jwt_required()
def update_profile():
    return update_user_profile_view(current_user, request.json)


@user_router.route("/me/address", methods=["POST", "GET"])
@jwt_required()
def address():
    match request.method.lower():
        case "post":
            return add_address_view(current_user, request.json)
        case "get":
            return get_all_address_view(current_user)


@user_router.route("/me/address/<int:address_id>", methods=["DELETE", "PUT"])
@jwt_required()
def specific_address(address_id):
    match request.method.lower():
        case "put":
            return update_address_view(current_user, request.json, address_id)  # noqa: F821
        case "delete":
            return delete_address_view(current_user, address_id)


@user_router.route("/me/payment-methods", methods=["POST", "GET"])
@jwt_required()
def payment_methods():
    match request.method.lower():
        case "post":
            return add_payment_method_view(current_user, request.json)
        case "get":
            return get_payment_methods_view(current_user)


@user_router.route(
    "/me/payment-methods/<int:payment_method_id>", methods=["DELETE", "PUT"]
)
@jwt_required()
def specific_payment_method(payment_method_id):
    match request.method.lower():
        case "put":
            return update_payment_method_view(
                current_user, request.json, payment_method_id
            )
        case "delete":
            return delete_payment_method_view(current_user, payment_method_id)