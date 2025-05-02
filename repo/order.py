from instance.database import db
from models.order import Order, OrderItem, OrderStatus, OrderStatusHistory, PaymentStatus, ShoppingCart, CartItem
from sqlalchemy.orm import contains_eager, joinedload
from models.product import Promotion, promotion_order_association


def get_shopping_cart_repo(user):
    cart = user.cart

    if not cart:
        cart = ShoppingCart(user_id=user.id)
        db.session.add(cart)
        db.session.commit()
        
    return cart


def get_cart_items_repo(cart_id):
    return (
        db.session.execute(
            db.select(CartItem)
            .join(CartItem.product)
            .options(contains_eager(CartItem.product))  # Eager load product data
            .where(CartItem.cart_id == cart_id)
        )
        .scalars()
        .all()
    )


def add_item_to_shopping_cart_repo(cart, cart_item):
    item = db.session.execute(
        db.select(CartItem).filter_by(
            cart_id=cart.id, 
            product_id=cart_item.product_id
        )
    ).scalar_one_or_none()

    if item:
        item.quantity += cart_item.quantity

    else:
        item = CartItem(
            cart_id=cart.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
        )
        db.session.add(item)
    
    db.session.commit()

    return item


def update_shopping_cart_item_repo(cart, update_data, product_id):
    item = db.one_or_404(
        db.select(CartItem).filter_by(
            cart_id=cart.id, 
            product_id=product_id
        ),
    )

    item.quantity = update_data.quantity
    db.session.commit()

    return item


def delete_shopping_cart_item_repo(cart, product_id):
    item = db.one_or_404(
        db.select(CartItem).filter_by(
            cart_id=cart.id, 
            product_id=product_id
        ),
    )

    db.session.delete(item)
    db.session.commit()

    return item


# ------------------------------- Order -------------------------------


def get_cart_with_items_and_product_repo(user_id):
    return db.session.execute(
        db.select(ShoppingCart)
        .options(joinedload(ShoppingCart.items).joinedload(CartItem.product))
        .where(ShoppingCart.user_id == user_id)
    ).scalars().first()


def checkout_order_repo(cart, order_data_validated, user_id, order_number):
    order = Order(
        user_id=user_id,
        order_number=order_number,
        status=OrderStatus.PENDING.value,
        total_amount=0,  # Will be calculated
        shipping_address_id=order_data_validated.shipping_address_id,
        billing_address_id=order_data_validated.billing_address_id,
        payment_method_id=order_data_validated.payment_method_id,
        payment_status=PaymentStatus.PENDING.value,
        notes=order_data_validated.notes,
    )

    db.session.add(order)
    db.session.flush()  # get order id
    return order


def process_order_items(order, item, product):
    # create order item
    order_item = OrderItem(
        order_id=order.id,
        product_id=item.product_id,
        quantity=item.quantity,
        unit_price=product.price,
        total_price=product.price * item.quantity,
        vendor_id=product.vendor_id,
    )
    db.session.add(order_item)

    # update product stock
    product.stock_quantity -= item.quantity

    # update order total amount
    order.total_amount += order_item.total_price


def add_order_status_history_repo(order, user_id):
    order_status_history = OrderStatusHistory(
        order_id=order.id,
        status=order.status,
        changed_by=user_id,
        notes="Order created from cart",
    )
    db.session.add(order_status_history)


def clear_shopping_cart_item_repo(item):
   db.session.delete(item)


def get_order_repo(user, order_number):
    return db.session.execute(
        db.select(Order)
        .options(
            joinedload(Order.items).joinedload(OrderItem.product),
            joinedload(Order.status_history),
        )
        .where(Order.order_number == order_number, Order.user_id == user.id)
    ).scalars().first()


def update_order_status_repo(order, status_request, user):
    order.status = status_request.status

    status_history = OrderStatusHistory(
        order_id=order.id,
        status=status_request.status,
        changed_by=user.id,
        notes=status_request.notes,
    )
    db.session.add(status_history)

    db.session.commit()

    return order


# ----------------------------------------------------------- Promotions -----------------------------------------------------------


def validate_promotion_repo(promo_code, cart_items):
    promotion = db.one_or_404(
        db.select(Promotion).filter_by(promo_code=promo_code),
        description=f"Promotion does not exist '{promo_code}'.",
    )

    # Check active status
    active = promotion.is_active
    if not active:
        return {"valid": False, "error": "Promotion not active"}

    # Get eligible product IDs for this promotion
    eligible_ids = [product.id for product in promotion.products] if promotion.products else []

    # convert to list
    cart_product_id_list = [item.product_id for item in cart_items]

    # Separate eligible vs non-eligible items
    eligible_items = [product_id for product_id in cart_product_id_list if product_id in eligible_ids]

    if not eligible_items:
        return {"valid": False, "error": "No eligible items in cart"}

    # Check usage limits
    if promotion.usage_limit and promotion.orders.count() >= promotion.usage_limit:
        return {"valid": False, "error": "Promo usage limit reached"}

    return {
        "valid": True,
        "promotion": promotion,
        "eligible_item_ids": eligible_items,
    }


def apply_promotion_to_order_repo(order, promotion, eligible_item_ids):
    # convert to list
    order_item_list = [item for item in order.items]

    print(order_item_list)

    eligible_order_items = [item for item in order_item_list if item.product_id in eligible_item_ids]

    print(eligible_order_items)

    # Calculate discount
    if promotion.promotion_type == "percentage_discount":
        subtotal = sum(item.total_price for item in eligible_order_items)
        print(subtotal)
        # discount will be less than or equal to max_discount
        discount = min(
            subtotal * (promotion.discount_value / 100),
            promotion.max_discount
        )
        print(discount)

    elif promotion.promotion_type == "fixed_discount":
        discount = promotion.discount_value * len(eligible_order_items)

    # Apply discount
    print(order.total_amount)
    order.total_amount -= discount
    print(order.total_amount, "after discount")

    if order.total_amount < 0:
        order.total_amount = 0

    # Record the promotion usage
    db.session.execute(
        promotion_order_association.insert().values(
            promotion_id=promotion.id,
            order_id=order.id,
            discount_applied=discount,
            eligible_items=str(eligible_item_ids),  # Store which items were discounted
        )
    )

    db.session.flush()

    return (order, discount) 


def get_promotions_repo(order_id):
    return db.session.execute(
        db.select(
            Promotion.title,
            promotion_order_association.c.discount_applied,
            promotion_order_association.c.eligible_items,
        )
        .join(Promotion)
        .where(promotion_order_association.c.order_id == order_id)
    ).all()