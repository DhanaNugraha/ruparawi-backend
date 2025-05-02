from datetime import datetime
import re
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import List, Optional
from decimal import Decimal

# -------------------------------------------------- Create Product --------------------------------------------------


class ProductCreateRequest(BaseModel):
    name: str
    description: str
    price: Decimal = Field(
        ..., gt=0, decimal_places=2
    )  # greater than 0, 2 decimal places
    category_id: int = None
    tags: List[str] = []
    sustainability_attributes: List[str] = []
    stock_quantity: int
    min_order_quantity: int = 1
    primary_image_url: str = None
    images: List[str] = []

    @field_validator("name")
    def validate_name(cls, value):
        if len(value) < 3 or len(value) > 100:
            raise ValueError("Name must be between 3 and 100 characters")

        return value

    @field_validator("description")
    def validate_description(cls, value):
        if len(value) < 10 or len(value) > 2000:
            raise ValueError("Description must be between 10 and 2000 characters")

        return value

    @field_validator("tags")
    def validate_tags(cls, value):
        if len(value) > 10:
            raise ValueError("Maximum of 10 tags allowed")

        return value

    @field_validator("sustainability_attributes")
    def validate_sustainability_attributes(cls, value):
        if len(value) > 5:
            raise ValueError("Maximum of 5 sustainability attributes allowed")

        return value

    @field_validator("stock_quantity")
    def validate_stock_quantity(cls, value):
        if value < 0:
            raise ValueError("Stock quantity cannot be negative")

        return value

    @field_validator("min_order_quantity")
    def validate_min_order_quantity(cls, value):
        if value < 1:
            raise ValueError("Minimum order quantity must be at least 1")

        return value
    
    @field_validator("primary_image_url")
    def validate_primary_image_url(cls, value):
        if not value:
            return value

        # Basic URL regex pattern
        url_pattern = re.compile(
            r"^(https?://)"  # http:// or https://
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # domain
            r"localhost|"  # localhost
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # or ip
            r"(?::\d+)?"  # optional port
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )

        if not url_pattern.match(value):
            raise ValueError("Invalid URL format")

        # Additional checks
        if len(value) > 500:
            raise ValueError("URL too long (max 500 chars)")
        
        return value.strip()

    @field_validator("images")
    def validate_images(cls, value):
        if not value:
            return value
        
        if value and len(value) > 4:
            raise ValueError("Maximum of 10 images allowed")

        for image in value:
            # Basic URL regex pattern
            url_pattern = re.compile(
                r"^(https?://)"  # http:// or https://
                r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # domain
                r"localhost|"  # localhost
                r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # or ip
                r"(?::\d+)?"  # optional port
                r"(?:/?|[/?]\S+)$",
                re.IGNORECASE,
            )

            if not url_pattern.match(image):
                raise ValueError("Invalid URL format")

            # Additional checks
            if len(image) > 500:
                raise ValueError("URL too long (max 500 chars)")
            
            image = image.strip()

        return value

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )
        

class ProductCreatedResponse(BaseModel):
    id: int
    name: str
    vendor_id: int

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )


# -------------------------------------------------- Get Products List --------------------------------------------------


class ProductListFilters(BaseModel):
    category_id: List[int] = None
    min_price: List[float] = None
    max_price: List[float] = None
    tags: List[str] = None

    @field_validator("min_price", "max_price")
    def validate_prices(cls, value):
        if value is not None and value[0] < 1:
            raise ValueError("Price cannot be negative")
        return value[0]

    @field_validator("category_id")
    def validate_category_id(cls, value):
        return value[0]

    model_config = ConfigDict(extra="ignore")


class ProductListResponse(BaseModel):
    id: int
    name: str
    price: float
    category_id: int | None  # no category
    tags: List[object] | str
    vendor_id: int
    primary_image_url: str | None = None

    @field_validator("tags")
    def validate_tags(cls, value):
        # repr to convert class object to string
        return repr([tag.name for tag in value])

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )


# -------------------------------------------------- Get Product Detail --------------------------------------------------


class ProductDetailResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category_id: int | None
    vendor_id: int
    tags: List[object] | str = []
    sustainability_attributes: List[object] | str = []
    stock_quantity: int
    min_order_quantity: int
    created_at: datetime
    updated_at: datetime
    # greater than or equal to 0 and less than or equal to 5
    average_rating: float | None
    review_count: int | None
    images: List[object] | str = []

    @field_validator("tags")
    def validate_tags(cls, value):
        # repr to convert class object to string
        return repr([tag.name for tag in value])

    @field_validator("sustainability_attributes")
    def validate_sustainability_attributes(cls, value):
        # repr to convert class object to string
        return repr([tag.name for tag in value])

    @field_validator("images")
    def validate_images(cls, value):
        # repr to convert class object to string
        return repr([{"image_url": image.image_url, "is_primary": image.is_primary} for image in value])


    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )


# -------------------------------------------------- Update Product --------------------------------------------------


class ProductUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    category_id: Optional[int] = None
    tags: Optional[List[str]] = None
    sustainability_attributes: Optional[List[str]] = None
    stock_quantity: Optional[int] = None
    min_order_quantity: Optional[int] = None
    is_active: Optional[bool] = None
    primary_image_url: Optional[str] = None
    images: Optional[List[str]] = None

    @field_validator("name")
    def validate_name(cls, value):
        if len(value) < 3 or len(value) > 100:
            raise ValueError("Name must be between 3 and 100 characters")

        return value

    @field_validator("description")
    def validate_description(cls, value):
        if len(value) < 10 or len(value) > 2000:
            raise ValueError("Description must be between 10 and 2000 characters")

        return value

    @field_validator("tags")
    def validate_tags(cls, value):
        if len(value) > 10:
            raise ValueError("Maximum of 10 tags allowed")

        return value

    @field_validator("sustainability_attributes")
    def validate_sustainability_attributes(cls, value):
        if len(value) > 5:
            raise ValueError("Maximum of 5 sustainability attributes allowed")

        return value

    @field_validator("stock_quantity")
    def validate_stock_quantity(cls, value):
        if value < 0:
            raise ValueError("Stock quantity cannot be negative")

        return value

    @field_validator("min_order_quantity")
    def validate_min_order_quantity(cls, value):
        if value < 1:
            raise ValueError("Minimum order quantity must be at least 1")

        return value

    @field_validator("primary_image_url")
    def validate_primary_image_url(cls, value):
        if not value:
            return value

        # Basic URL regex pattern
        url_pattern = re.compile(
            r"^(https?://)"  # http:// or https://
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # domain
            r"localhost|"  # localhost
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # or ip
            r"(?::\d+)?"  # optional port
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )

        if not url_pattern.match(value):
            raise ValueError("Invalid URL format")

        # Additional checks
        if len(value) > 500:
            raise ValueError("URL too long (max 500 chars)")

        return value.strip()

    @field_validator("images")
    def validate_images(cls, value):
        if not value:
            return value

        if value and len(value) > 4:
            raise ValueError("Maximum of 10 images allowed")

        for image in value:
            # Basic URL regex pattern
            url_pattern = re.compile(
                r"^(https?://)"  # http:// or https://
                r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # domain
                r"localhost|"  # localhost
                r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # or ip
                r"(?::\d+)?"  # optional port
                r"(?:/?|[/?]\S+)$",
                re.IGNORECASE,
            )

            if not url_pattern.match(image):
                raise ValueError("Invalid URL format")

            # Additional checks
            if len(image) > 500:
                raise ValueError("URL too long (max 500 chars)")

            image = image.strip()

        return value


# -------------------------------------------------- Delete Product --------------------------------------------------


class ProductDeleteResponse(BaseModel):
    id: int
    name: str
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )


# -------------------------------------------------- Get vendor products --------------------------------------------------


class VendorProductsResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category_id: int | None
    vendor_id: int
    tags: List[object] | str
    sustainability_attributes: List[object] | str
    stock_quantity: int
    min_order_quantity: int
    created_at: datetime
    updated_at: datetime
    # greater than or equal to 0 and less than or equal to 5
    average_rating: float | None
    review_count: int | None
    is_active: bool
    images: List[object] | str = []

    @field_validator("tags")
    def validate_tags(cls, value):
        # repr to convert class object to string
        return repr([tag.name for tag in value])

    @field_validator("sustainability_attributes")
    def validate_sustainability_attributes(cls, value):
        # repr to convert class object to string
        return repr([tag.name for tag in value])
    
    @field_validator("images")
    def validate_images(cls, value):
        # repr to convert class object to string
        return repr([{"image_url": image.image_url, "is_primary": image.is_primary} for image in value])

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )


# -------------------------------------------------- Wishlist --------------------------------------------------


class WishlistProductResponse(BaseModel):
    id: int
    name: str
    price: float
    average_rating: Optional[float] = None
    primary_image: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )


class WishlistResponse(BaseModel):
    products: List[WishlistProductResponse]
    count: Optional[int]

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )


# -------------------------------------------------- Promotion --------------------------------------------------


class PromotionListResponse(BaseModel):
    id: int
    is_active: bool
    promotion_type: str
    title: str
    start_date: datetime
    end_date: datetime
    promo_code: str
    image_url: Optional[str]
    usage_limit: int
    products: List[object] | str = []

    @field_validator("products")
    def validate_product_ids(cls, value):
        # repr to convert class object to string
        return repr([product.id for product in value])

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )


class PromotionDetailResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    promo_code: str
    discount_value: float
    promotion_type: str
    start_date: datetime
    end_date: datetime
    image_url: Optional[str] = None
    max_discount: Optional[float] = None  # Required for percentage discounts
    usage_limit: Optional[int]
    products: List[object] | str = []
    created_at: datetime
    updated_at: datetime
    is_active: bool

    @field_validator("products")
    def validate_product_ids(cls, value):
        # repr to convert class object to string
        return repr([product.id for product in value])

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )