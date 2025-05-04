from datetime import date, datetime
import re
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator

from models.product import PromotionType
from shared.time import datetime_from_date_string


class CategoryCreate(BaseModel):
    parent_category_id: Optional[int] = None
    name: str
    description: Optional[str] = None

    @field_validator("name")
    def validate_name(cls, value):
        if len(value) < 2 or len(value) > 50:
            raise ValueError("Name must be between 2 and 50 characters")
        
        return value

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )


class CategoryResponse(BaseModel):
    id: Optional[int] = None
    parent_category_id: Optional[int] = None
    subcategories: Optional[List["CategoryResponse"]] = [] #subcategory is a nested class
    name: str
    description: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )


class CategoryTreeResponse(BaseModel):
    categories: List[CategoryResponse] 
    

class CategoryUpdate(BaseModel):
    parent_category_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None

    @field_validator("name")
    def validate_name(cls, value):
        if len(value) < 2 or len(value) > 50:
            raise ValueError("Name must be between 2 and 50 characters")
        
        return value

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )

class CategoryUpdateResponse(BaseModel):
    id: Optional[int] = None
    parent_category_id: Optional[int] = None
    name: str
    description: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )


class VendorApprovalRequest(BaseModel):
    action: str 
    reason: Optional[str] = None

    @field_validator("action")
    def validate_action(value):
        pattern = r"approve|reject"

        if not re.fullmatch(pattern, value):
            raise ValueError("Invalid action format")

        return value
    
    @field_validator("reason")
    def validate_reason(cls, value):
        if value and len(value) > 500:
            raise ValueError("reason cannot exceed 500 characters")
        
        return value

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )


class AdminLogsResponse(BaseModel):
    id: int
    admin_id: int
    action: str
    timestamp: datetime

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )


# ------------------------------------------------------------------ Promotion ------------------------------------------------------------------


class PromotionCreate(BaseModel):
    title: str
    description: Optional[str] = None
    promo_code: str
    discount_value: float
    promotion_type: str
    start_date: date | str
    end_date: date | str
    image_url: Optional[str] = None
    max_discount: Optional[float] = None  # Required for percentage discounts
    usage_limit: Optional[int] = None
    product_ids: List[int] = []

    @field_validator("title")
    def validate_title(cls, value):
        value = value.strip()
        if len(value) < 2 or len(value) > 100:
            raise ValueError("Title must be between 2 and 100 characters")
        return value

    @field_validator("promo_code")
    def validate_promo_code(cls, value):
        if len(value) > 20:
            raise ValueError("Promo code must be less than 20 characters")
        return value

    @field_validator("discount_value")
    def validate_discount_value(cls, value):
        if value <= 0:
            raise ValueError("Discount value must be greater than 0")
        return value

    @field_validator("promotion_type")
    def validate_promotion_type(cls, value):
        # Get all valid enum values
        valid_values = [enum.value for enum in PromotionType]

        # Check if the string matches any enum value
        if value not in valid_values:
            raise ValueError(
                f"Invalid promotion type '{value}'. Must be one of: {valid_values}"
            )
        return value  # Return the validated string
    
    @field_validator("start_date")
    def validate_start_date(cls, value):
        return datetime_from_date_string(value)
    
    @field_validator("end_date")
    def validate_end_date(cls, value):
        return datetime_from_date_string(value)

    @field_validator("image_url")
    def validate_image_url(cls, value):
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

    @field_validator("usage_limit")
    def validate_usage_limit(cls, value):
        if value <= 0:
            raise ValueError("Usage limit must be greater than 0")
        return value

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )


class PromotionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    promo_code: Optional[str] = None
    discount_value: Optional[float] = None
    promotion_type: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    image_url: Optional[str] = None
    max_discount: Optional[float] = None  # Required for percentage discounts
    usage_limit: Optional[int] = None
    product_ids: List[int] = None

    @field_validator("title")
    def validate_title(cls, value):
        value = value.strip()
        if len(value) < 2 or len(value) > 100:
            raise ValueError("Title must be between 2 and 100 characters")
        return value

    @field_validator("promo_code")
    def validate_promo_code(cls, value):
        if len(value) > 20:
            raise ValueError("Promo code must be less than 20 characters")
        return value

    @field_validator("discount_value")
    def validate_discount_value(cls, value):
        if value <= 0:
            raise ValueError("Discount value must be greater than 0")
        return value

    @field_validator("promotion_type")
    def validate_promotion_type(cls, value):
        # Get all valid enum values
        valid_values = [enum.value for enum in PromotionType]

        # Check if the string matches any enum value
        if value not in valid_values:
            raise ValueError(
                f"Invalid promotion type '{value}'. Must be one of: {valid_values}"
            )
        return value  # Return the validated string

    @field_validator("image_url")
    def validate_image_url(cls, value):
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

    @field_validator("usage_limit")
    def validate_usage_limit(cls, value):
        if value <= 0:
            raise ValueError("Usage limit must be greater than 0")
        return value

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )



