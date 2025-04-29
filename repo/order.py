from instance.database import db
from models.order import ShoppingCart, CartItem
from models.product import Product
from sqlalchemy.orm import contains_eager


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
