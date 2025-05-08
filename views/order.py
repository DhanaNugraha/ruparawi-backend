import uuid
from flask import json, jsonify
from pydantic import ValidationError
from instance.database import db
from repo.order import add_item_to_shopping_cart_repo, add_order_status_history_repo, apply_promotion_to_order_repo, checkout_order_repo, clear_shopping_cart_item_repo, delete_shopping_cart_item_repo, get_all_orders_repo, get_cart_items_repo, get_cart_with_items_and_product_repo, get_order_repo, get_promotions_repo, get_shopping_cart_repo, pre_checkout_promotion_calculation, process_order_items, update_order_status_repo, update_shopping_cart_item_repo, validate_promotion_repo
from repo.product import get_product_detail_repo, verify_product_repo
from schemas.order import AddCartItemResponse, CartResponse, CartItemUpdate, CartItemCreate, OrderCreate, OrderResponse, OrderStatusUpdate
from shared.time import now


# ------------------------------------------------------ Get shopping cart --------------------------------------------------


def get_shopping_cart_view(user):
    try:
        cart = get_shopping_cart_repo(user)

        cart_items = get_cart_items_repo(cart.id)

        cart_items_response = [
            {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "product": {
                    "name": item.product_name,
                    "price": item.price,
                    "image_url": item.image_url,
                },
            } for item in cart_items
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


# ------------------------------------------------------ Checkout order --------------------------------------------------


def checkout_order_view(user, order_request):
    try:
        order_data_validated = OrderCreate.model_validate(order_request)

        # get cart with items and product
        cart = get_cart_with_items_and_product_repo(user.id)

        # save cart items for promotions later
        cart_items = cart.items

        # Generate unique order number
        order_number = generate_order_number()

        # Create order
        order = checkout_order_repo(cart, order_data_validated, user.id, order_number)

        # convert cart items to order items
        for item in cart_items:
            product = item.product

            # Recheck product stock and status
            issue, status = verify_product_repo(product, item.quantity)

            if status is False:
                return jsonify(
                    {
                        "message": f"{product.name} cannot be ordered",
                        "issue": issue,
                        "success": False,
                    }
                ), 400

            # create order item, update product stock, update order total amount
            process_order_items(order, item, product)

            # delete cart item
            clear_shopping_cart_item_repo(item)

        promotion_response = {}

        # validate promotion
        if order_data_validated.promotion_code:
            promotion = validate_promotion_repo(
                order_data_validated.promotion_code, cart_items
            )

            if promotion.get("error"):  
                return jsonify(
                    {
                        "message": promotion.get("error"),
                        "success": False,
                        "location": "view checkout order repo",
                    }
                ), 400

            order, discount = apply_promotion_to_order_repo(order, promotion.get("promotion"), promotion.get("eligible_item_ids"))

            promotion_response = {
                "title": promotion.get("promotion").title,
                "discount": round(discount, 2), 
                "eligible_items_ids": promotion.get("eligible_item_ids"),
            }

        # add order status history
        add_order_status_history_repo(order, user.id)

        # commit
        db.session.commit()

        return jsonify(
            {
                "message": "Order checked out successfully",
                "order": OrderResponse.model_validate(order).model_dump(),
                "applied_promotion": promotion_response,
                "success": True,
            }
        ), 201

    except ValidationError as e:
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view checkout order request validation",
            }
        ), 400

    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view checkout order repo",
            }
        ), 500


def generate_order_number():
    # Format: YYMMDD + first 12 chars of UUID = 18 characters total
    date_part = now().strftime("%y%m%d")
    uuid_part = str(uuid.uuid4().hex)[:12].upper()
    return f"{date_part}{uuid_part}"  # Example: "240523A1B2C3D4E5F6"


# ------------------------------------------------------ Pre Checkout order --------------------------------------------------


def pre_checkout_order_view(user, promotion_code):
    try:
        promotion_code = promotion_code.get("promotion_code")
        # get cart with items and product
        cart = get_cart_with_items_and_product_repo(user.id)

        # save cart items for promotions later
        cart_items = cart.items

        # Calculate total amount
        total_amount = 0

        # convert cart items to order items
        for item in cart_items:
            total_amount += item.product.price * item.quantity

        promotion_response = {
                "title": None,
                "total_price": total_amount,
                "discount": None,
                "eligible_items_ids": None,
            }

        # validate promotion
        if promotion_code:
            promotion = validate_promotion_repo(
                promotion_code, cart_items
            )

            if promotion.get("error"):
                return jsonify(
                    {
                        "message": promotion.get("error"),
                        "promotion": promotion_response,
                        "success": True,
                    }
                ), 200

            total_price, discount = pre_checkout_promotion_calculation(
                cart_items,
                promotion.get("promotion"),
                promotion.get("eligible_item_ids"),
                total_amount,
            )

            promotion_response = {
                "title": promotion.get("promotion").title,
                "total_price": round(total_price, 2),
                "discount": round(discount, 2),
                "eligible_items_ids": promotion.get("eligible_item_ids"),
            }

        return jsonify(
            {
                "message": "Order calculated out successfully",
                "promotion": promotion_response,
                "success": True,
            }
        ), 200

    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view pre-checkout order repo",
            }
        ), 500
    

# ------------------------------------------------------ Get order --------------------------------------------------


def get_order_view(user, order_number):
    try:
        order = get_order_repo(user, order_number)

        promotions = get_promotions_repo(order.id)

        return jsonify(
            {
                "message": "Order fetched successfully",
                "order": OrderResponse.model_validate(order).model_dump(),
                "success": True,
                "applied_promotions": [{
                        "title": promotion.title,
                        "discount": round(promotion.discount_applied, 2),
                        "eligible_items": json.loads(promotion.eligible_items)
                    } for promotion in promotions]
            }
        ), 200

    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view get order repo",
            }
        ), 500
    

# ------------------------------------------------------ Get all order --------------------------------------------------


def get_all_orders_view(user):
    try:

        orders = get_all_orders_repo(user)

        return jsonify(
            {
                "success": True,
                "orders": [
                    OrderResponse.model_validate(order).model_dump() for order in orders
                ],
            }
        ), 200

    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view get all orders repo",
            }
        ), 500


# ------------------------------------------------------ Update item in cart --------------------------------------------------


def update_order_status_view(user, order_status_request, order_number):
    try:
        order_status = OrderStatusUpdate.model_validate(order_status_request)

        order = get_order_repo(user, order_number)

        updated_order = update_order_status_repo(order, order_status, user)

        return jsonify(
            {
                "message": "Order status updated successfully",
                "order": OrderResponse.model_validate(updated_order).model_dump(),
                "success": True,
            }
        ), 200

    except ValidationError as e:
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view update order status request validation",
            }
        ), 400

    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view update order status repo",
            }
        ), 500
    

