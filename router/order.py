from flask import Blueprint, request
from flask_jwt_extended import current_user, jwt_required
from views.order import add_item_to_shopping_cart_view, checkout_order_view, delete_shopping_cart_item_view, get_all_orders_view, get_order_view, get_shopping_cart_view, pre_checkout_order_view, update_order_status_view, update_shopping_cart_item_view


order_router = Blueprint("order_router", __name__, url_prefix="/order")

# ------------------------------------------------------------------ Cart --------------------------------------------------

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


# -------------------------------------------------------------------------- Order -----------------------------------------------


@order_router.route("/checkout", methods=["POST"])
@jwt_required()
def checkout_order():
    return checkout_order_view(current_user, request.json)


@order_router.route("/pre-checkout", methods=["POST"])
@jwt_required()
def pre_checkout_order():
    return pre_checkout_order_view(current_user, request.json)


@order_router.route("/<string:order_number>", methods=["GET"])
@jwt_required()
def get_order(order_number):
    return get_order_view(current_user, order_number)


@order_router.route("/<string:order_number>", methods=["PUT"])
@jwt_required()
def update_order_status(order_number):
    return update_order_status_view(current_user, request.json, order_number)


@order_router.route("", methods=["GET"])
@jwt_required()
def get_all_orders():
    return get_all_orders_view(current_user)