from instance.database import db
from models.order import Order, OrderItem, OrderStatus, OrderStatusHistory, PaymentStatus, ShoppingCart, CartItem
from sqlalchemy.orm import contains_eager, joinedload


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