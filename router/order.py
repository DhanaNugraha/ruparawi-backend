from flask import Blueprint, request
from flask_jwt_extended import current_user, jwt_required
from views.order import add_item_to_shopping_cart_view, delete_shopping_cart_item_view, get_shopping_cart_view, update_shopping_cart_item_view


order_router = Blueprint("order_router", __name__, url_prefix="/order")

@order_router.route("/cart", methods=["GET"])
@jwt_required()
def get_shopping_cart():
    return get_shopping_cart_view(current_user)


@order_router.route("/cart/item", methods=["POST"])
@jwt_required()
def add_item_to_shopping_cart():
    return add_item_to_shopping_cart_view(current_user, request.json)


@order_router.route("/cart/item/<int:product_id>", methods=["PUT"])
@jwt_required()
def update_shopping_cart_item(product_id):
    return update_shopping_cart_item_view(current_user, request.json, product_id)


@order_router.route("/cart/item/<int:product_id>", methods=["DELETE"])
@jwt_required()
def delete_shopping_cart_item(product_id):
    return delete_shopping_cart_item_view(current_user, product_id)