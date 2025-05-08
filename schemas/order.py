from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator

from models.order import OrderStatus


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1

    @field_validator("product_id")
    def validate_product_id(cls, value):
        if value < 0:
            raise ValueError("Product ID cannot be negative")

        return value

    @field_validator("quantity")
    def validate_quantity(cls, value):
        if value < 0 or value > 1000:
            raise ValueError("Quantity must be between 1 and 1000")

        return value


class CartItemUpdate(BaseModel):
    quantity: int

    @field_validator("quantity")
    def validate_quantity(cls, value):
        if value < 0 or value > 1000:
            raise ValueError("Quantity must be between 1 and 1000")

        return value


class CartResponse(BaseModel):
    user_id: int

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )


class AddCartItemResponse(BaseModel):
    product_id: int
    quantity: int

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )


# ------------------------------------------------------------------ Order --------------------------------------------------


class OrderCreate(BaseModel):
    shipping_address_id: int
    billing_address_id: Optional[int] = None
    payment_method_id: int
    promotion_code: Optional[str] = None
    notes: Optional[str] = None

    @field_validator("shipping_address_id")
    def validate_shipping_address_id(cls, value):
        if value < 0:
            raise ValueError("Shipping address ID cannot be negative")

        return value

    @field_validator("payment_method_id")
    def validate_payment_method_id(cls, value):
        if value < 0:
            raise ValueError("Payment method ID cannot be negative")

        return value

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )


class OrderStatusHistoryResponse(BaseModel):
    id: int
    status: str
    changed_at: datetime
    changed_by: Optional[int]
    notes: Optional[str]

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )


class OrderResponse(BaseModel):
    id: int
    order_number: str
    status: str
    total_amount: float
    created_at: Optional[datetime] = None
    items: list | str
    status_history: list | str

    @field_validator("items")
    def validate_items(cls, value):
        return repr(
            [
                {
                    "name": item.product.name,
                    "image_url": next(
                        (
                            img.image_url
                            for img in item.product.images
                            if img.is_primary
                        ),
                        None,
                    ),
                }
                for item in value
            ]
        )

    @field_validator("status_history")
    def validate_status_history(cls, value):
        return repr([item.status for item in value])

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )


class OrderStatusUpdate(BaseModel):
    status: str
    notes: Optional[str] = None

    @field_validator("status")
    def validate_status(cls, value):
        # Get all valid enum values
        valid_values = [enum.value for enum in OrderStatus]

        # Check if the string matches any enum value
        if value not in valid_values:
            raise ValueError(
                f"Invalid status '{value}'. Must be one of: {valid_values}"
            )
        return value  # Return the validated string

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )
