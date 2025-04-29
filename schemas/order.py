from pydantic import BaseModel, ConfigDict, field_validator


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


class ProductBase(BaseModel):
    name: str
    price: float

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )

class CartItemResponse(BaseModel):
    product_id: int
    quantity: int
    product: ProductBase

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )


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
