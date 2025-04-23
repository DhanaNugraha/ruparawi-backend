from instance.database import db
from .base import BaseModel
from enum import Enum as PyEnum

class OrderStatus(PyEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class PaymentStatus(PyEnum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"

class ShoppingCart(db.Model, BaseModel):
    __tablename__ = "shopping_carts"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Relationships
    items = db.relationship("CartItem", backref="cart", lazy=True)


class CartItem(db.Model, BaseModel):
    __tablename__ = "cart_items"

    cart_id = db.Column(db.Integer, db.ForeignKey("shopping_carts.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


class Order(db.Model, BaseModel):
    __tablename__ = "orders"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), nullable=False, default=OrderStatus.PENDING.value)  
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    shipping_address_id = db.Column(db.Integer, db.ForeignKey("user_addresses.id"))
    billing_address_id = db.Column(db.Integer, db.ForeignKey("user_addresses.id"))
    payment_method_id = db.Column(db.Integer, db.ForeignKey("user_payment_methods.id"))
    payment_status = db.Column(db.String(20), nullable=False, default=PaymentStatus.PENDING.value) 
    tracking_number = db.Column(db.String(100))
    estimated_delivery_date = db.Column(db.DateTime)
    actual_delivery_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)

    # Relationships
    items = db.relationship("OrderItem", backref="order", lazy=True)
    status_history = db.relationship("OrderStatusHistory", backref="order", lazy=True)


class OrderItem(db.Model, BaseModel):
    __tablename__ = "order_items"

    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class OrderStatusHistory(db.Model, BaseModel):
    __tablename__ = "order_status_history"

    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    changed_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    notes = db.Column(db.Text)
