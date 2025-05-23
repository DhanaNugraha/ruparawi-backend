from datetime import timezone
from enum import Enum
from instance.database import db
from shared.time import now
from .base import BaseModel


# ------------------------------------- Enum --------------------------------------
class PromotionType(Enum):
    PERCENTAGE_DISCOUNT = "percentage_discount"
    FIXED_DISCOUNT = "fixed_discount"


#------------------- assosiation tables for many to many relationship----------------------
product_tag_association = db.Table(
    "product_tag_association",
    db.Column("product_id", db.Integer, db.ForeignKey("products.id")),
    db.Column("tag_id", db.Integer, db.ForeignKey("product_tags.id")),
)

product_sustainability_association = db.Table(
    "product_sustainability_association",
    db.Column("product_id", db.Integer, db.ForeignKey("products.id")),
    db.Column("sustainability_attribute_id", db.Integer, db.ForeignKey("sustainability_attributes.id")),
)

wishlist_association = db.Table(
    "wishlist_association",
    db.Column("wishlist_id", db.Integer, db.ForeignKey("wishlists.id"), primary_key=True),
    db.Column("product_id", db.Integer, db.ForeignKey("products.id"), primary_key=True),
    db.Column("created_at", db.DateTime, server_default=db.func.now()),
)

promotion_product_association = db.Table(
    "promotion_product_association",
    db.Column(
        "promotion_id", db.Integer, db.ForeignKey("promotions.id"), primary_key=True
    ),
    db.Column("product_id", db.Integer, db.ForeignKey("products.id"), primary_key=True),
    db.Column("created_at", db.DateTime, default=now()),
)

promotion_category_association = db.Table(
    "promotion_category_association",
    db.Column(
        "promotion_id", db.Integer, db.ForeignKey("promotions.id"), primary_key=True
    ),
    db.Column(
        "category_id",
        db.Integer,
        db.ForeignKey("product_categories.id"),
        primary_key=True,
    ),
    db.Column("created_at", db.DateTime, default=now()),
)

promotion_order_association = db.Table(
    "promotion_order_association",
    db.Column(
        "promotion_id", db.Integer, db.ForeignKey("promotions.id"), primary_key=True
    ),
    db.Column("order_id", db.Integer, db.ForeignKey("orders.id"), primary_key=True),
    db.Column(
        "discount_applied", db.Numeric(10, 2)
    ),  # Track how much discount was given
    db.Column("created_at", db.DateTime, server_default=db.func.now()),
    db.Column("eligible_items", db.Text),
)

# -------------------------------------------------------

class ProductCategory(db.Model, BaseModel):
    __tablename__ = "product_categories"

    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text)
    parent_category_id = db.Column(db.Integer, db.ForeignKey("product_categories.id"))
    is_active = db.Column(db.Boolean, default=True)

    # Self-referential relationship
    subcategories = db.relationship(
        "ProductCategory",
        backref=db.backref("parent", remote_side="ProductCategory.id"),
    )
    # Relationship
    products = db.relationship("Product", backref="category", lazy=True)


class SustainabilityAttribute(db.Model, BaseModel):
    __tablename__ = "sustainability_attributes"

    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    icon_url = db.Column(db.String(255))


class ProductTag(db.Model, BaseModel):
    __tablename__ = "product_tags"

    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)


class Product(db.Model, BaseModel):
    __tablename__ = "products"

    vendor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("product_categories.id"))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    min_order_quantity = db.Column(db.Integer, default=1)
    average_rating = db.Column(db.Numeric(3, 2), default=0.00)
    review_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    images = db.relationship("ProductImage", backref="product", lazy=True)
    sustainability_attributes = db.relationship(
        "SustainabilityAttribute", secondary=product_sustainability_association, backref="product", lazy=True
    )
    tags = db.relationship("ProductTag", secondary=product_tag_association, backref="product", lazy=True)
    cart_items = db.relationship("CartItem", backref="product", lazy=True)
    order_items = db.relationship("OrderItem", backref="product", lazy=True)

    def update_rating_stats(self):
        # Recalculates average rating and review count
        reviews = self.reviews
        if reviews:
            total = sum(review.rating for review in reviews)
            self.average_rating = round(total / len(reviews), 2)
            self.review_count = len(reviews)
        else:
            self.average_rating = 0.00
            self.review_count = 0


class ProductImage(db.Model, BaseModel):
    __tablename__ = "product_images"

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)


class Wishlist(db.Model, BaseModel):
    __tablename__ = "wishlists"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    products = db.relationship(
        "Product",
        secondary=wishlist_association,
        backref="wishlisted_by"
    )

    def add_product(self, product):
        if not self.has_product(product):
            self.products.append(product)
            return True
        return False

    def remove_product(self, product):
        if self.has_product(product):
            self.products.remove(product)
            return True
        return False

    def has_product(self, product):
        return product in self.products


# ------------------------------------------------------- Promotions


class Promotion(db.Model, BaseModel):
    __tablename__ = "promotions"

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    promo_code = db.Column(db.String(20), unique=True, nullable=False)
    discount_value = db.Column(db.Numeric(10, 2))  # Percentage or fixed amount
    promotion_type = db.Column(db.String(25), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    image_url = db.Column(db.String(255))
    max_discount = db.Column(db.Numeric(10, 2))  # For percentage discounts
    usage_limit = db.Column(db.Integer)  # Max number of uses (optional)

    # Relationships
    products = db.relationship(
        "Product", secondary="promotion_product_association", backref="promotions"
    )

    categories = db.relationship(
        "ProductCategory",
        secondary="promotion_category_association",
        backref="promotions"
    )

    admin = db.relationship("User", backref="created_promotions")

    orders = db.relationship(
        "Order",
        secondary=promotion_order_association,
        backref=db.backref("applied_promotions", lazy="dynamic"),
        lazy="dynamic"
    )

    @property
    def is_active(self):
        now_ = now()
        return (
            self.start_date.replace(tzinfo=timezone.utc)
            <= now_
            <= self.end_date.replace(tzinfo=timezone.utc)
        )
    

# ------------------------------------------------------- Currency handler ------------------------------------------------

class Currency(db.Model, BaseModel):
    __tablename__ = "currencies"

    code = db.Column(db.String(3), primary_key=True)  # ISO 4217 (USD, EUR, etc.)
    name = db.Column(db.String(50))
    conversion_rate = db.Column(db.Numeric(10, 6))  # Relative to base currency