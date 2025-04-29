from flask import jsonify
from pydantic import ValidationError
from instance.database import db
from repo.order import add_item_to_shopping_cart_repo, delete_shopping_cart_item_repo, get_cart_items_repo, get_shopping_cart_repo, update_shopping_cart_item_repo
from repo.product import get_product_detail_repo
from schemas.order import AddCartItemResponse, CartItemResponse, CartResponse, CartItemUpdate, CartItemCreate


# ------------------------------------------------------ Get shopping cart --------------------------------------------------


def get_shopping_cart_view(user):
    try:
        cart = get_shopping_cart_repo(user)

        cart_items = get_cart_items_repo(cart.id)

        cart_items_response = [
            CartItemResponse.model_validate(cart_item).model_dump() for cart_item in cart_items
        ]

        return jsonify(
            {
                "success": True, 
                "cart": CartResponse.model_validate(cart).model_dump(), 
                "cart_items": cart_items_response}
        ), 200

    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view get shopping cart repo",
            }
        ), 500


# ------------------------------------------------------ Add item to cart --------------------------------------------------


def add_item_to_shopping_cart_view(user, cart_item_request):
    try:
        cart_item_data_validated = CartItemCreate.model_validate(cart_item_request)

        cart = get_shopping_cart_repo(user)

        # get product and check stock
        product = get_product_detail_repo(cart_item_data_validated.product_id)

        if product.stock_quantity < cart_item_data_validated.quantity:
            return jsonify(
                {
                    "message": "Not enough stock",
                    "stock" : product.stock_quantity,
                    "success": False,
                }
            ), 400
        

        # add item to CartItem
        item = add_item_to_shopping_cart_repo(cart, cart_item_data_validated)

        return jsonify(
            {
                "message": "Item added to cart successfully",
                "cart_item": AddCartItemResponse.model_validate(item).model_dump(),
                "success": True,
            }
        ), 201

    # test with validator
    except ValidationError as e:
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view add item to cart request validation",
            }
        ), 400

    # test with product id given
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view add item to cart repo",
            }
        ), 500
    

# ------------------------------------------------------ Update item in cart --------------------------------------------------


def update_shopping_cart_item_view(user, cart_item_request, product_id):
    try:
        item_update_data_validated = CartItemUpdate.model_validate(cart_item_request)

        cart = get_shopping_cart_repo(user)

        # get product and check stock
        product = get_product_detail_repo(product_id)

        if product.stock_quantity < item_update_data_validated.quantity:
            return jsonify(
                {
                    "message": "Not enough stock",
                    "stock" : product.stock_quantity,
                    "success": False,
                }
            ), 400
        
        # add item to CartItem
        item = update_shopping_cart_item_repo(cart, item_update_data_validated, product_id)
        
        return jsonify(
            {
                "message": "Cart item updated successfully",
                "cart_item": AddCartItemResponse.model_validate(item).model_dump(),
                "success": True,
            }
        ), 200

    # test with validator
    except ValidationError as e:
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view update item in cart request validation",
            }
        ), 400

    # test with item id given
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view update item in cart repo",
            }
        ), 500
    

# ------------------------------------------------------ Delete item in cart --------------------------------------------------


def delete_shopping_cart_item_view(user, product_id):
    try:
        cart = get_shopping_cart_repo(user)

        delete_shopping_cart_item_repo(cart, product_id)

        return jsonify(
            {
                "message": "Cart item deleted successfully",
                "success": True,
            }
        ), 200

    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "message": str(e),
                "success": False, 
                "location": "view delete item in cart repo",
            }
        ), 500