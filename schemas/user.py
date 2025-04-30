import re
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator
from datetime import date, datetime

from models.user import PaymentType
from shared.time import date_now

# -------------------------------------------------- Register User --------------------------------------------------
class UserRoleResponse(BaseModel):
    name: str

    # pydantic can read ORM objects with this
    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )

class PublicUserProfileResponse(BaseModel):
    id: int
    username: str
    first_name: str | None
    last_name: str | None
    profile_image_url: str | None
    bio: str | None
    role: List[UserRoleResponse]
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )


# -------------------------------------------------- Update User --------------------------------------------------


class UserProfileUpdateRequest(BaseModel):
    bio: str | None = None
    profile_image_url: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    password: str | None = None

    @field_validator("bio")
    def validate_bio(cls, value):
        if value and len(value) > 500:
            raise ValueError("Bio cannot exceed 500 characters")
        return value

    @field_validator("profile_image_url")
    def validate_url(cls, value):
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
    
    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters")

        return value

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )


# -------------------------------------------------- Create user address --------------------------------------------------


class UserAddressCreate(BaseModel):
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: str
    postal_code: str
    country: str
    is_default: bool = False

    @field_validator("address_line1")
    def validate_address_line1(cls, value):
        if len(value) < 1 or len(value) > 100:
            raise ValueError("Address line 1 cannot exceed 100 characters")
        return value

    @field_validator("address_line2")
    def validate_address_line2(cls, value):
        if value and len(value) > 100:
            raise ValueError("Address line 2 cannot exceed 100 characters")
        return value

    @field_validator("city")
    def validate_city(cls, value):
        if len(value) < 1 or len(value) > 50:
            raise ValueError("City cannot exceed 50 characters")
        return value

    @field_validator("state")
    def validate_state(cls, value):
        if len(value) < 1 or len(value) > 50:
            raise ValueError("State cannot exceed 50 characters")
        return value

    @field_validator("postal_code")
    def validate_postal_code(cls, value):
        if len(value) < 1 or len(value) > 20:
            raise ValueError("Postal code cannot exceed 20 characters")
        return value

    @field_validator("country")
    def validate_country(cls, value):
        if len(value) < 1 or len(value) > 50:
            raise ValueError("Country cannot exceed 50 characters")
        return value

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )


# -------------------------------------------------- update user address --------------------------------------------------


class UserAddressUpdate(BaseModel):
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    is_default: Optional[bool] = None

    @field_validator("address_line1")
    def validate_address_line1(cls, value):
        if value and len(value) < 1 or len(value) > 100:
            raise ValueError("Address line 1 cannot exceed 100 characters")
        return value

    @field_validator("address_line2")
    def validate_address_line2(cls, value):
        if value and len(value) > 100:
            raise ValueError("Address line 2 cannot exceed 100 characters")
        return value

    @field_validator("city")
    def validate_city(cls, value):
        if value and len(value) < 1 or len(value) > 50:
            raise ValueError("City cannot exceed 50 characters")
        return value

    @field_validator("state")
    def validate_state(cls, value):
        if value and len(value) < 1 or len(value) > 50:
            raise ValueError("State cannot exceed 50 characters")
        return value

    @field_validator("postal_code")
    def validate_postal_code(cls, value):
        if value and len(value) < 1 or len(value) > 20:
            raise ValueError("Postal code cannot exceed 20 characters")
        return value

    @field_validator("country")
    def validate_country(cls, value):
        if value and len(value) < 1 or len(value) > 50:
            raise ValueError("Country cannot exceed 50 characters")
        return value

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )


# -------------------------------------------------- Get all user address --------------------------------------------------


class UserAddressResponse(BaseModel):
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: str
    postal_code: str
    country: str
    is_default: bool = False
    id: int
    user_id: int

    @field_validator("address_line1")
    def validate_address_line1(cls, value):
        if len(value) < 1 or len(value) > 100:
            raise ValueError("Address line 1 cannot exceed 100 characters")
        return value

    @field_validator("address_line2")
    def validate_address_line2(cls, value):
        if value and len(value) > 100:
            raise ValueError("Address line 2 cannot exceed 100 characters")
        return value

    @field_validator("city")
    def validate_city(cls, value):
        if len(value) < 1 or len(value) > 50:
            raise ValueError("City cannot exceed 50 characters")
        return value

    @field_validator("state")
    def validate_state(cls, value):
        if len(value) < 1 or len(value) > 50:
            raise ValueError("State cannot exceed 50 characters")
        return value

    @field_validator("postal_code")
    def validate_postal_code(cls, value):
        if len(value) < 1 or len(value) > 20:
            raise ValueError("Postal code cannot exceed 20 characters")
        return value

    @field_validator("country")
    def validate_country(cls, value):
        if len(value) < 1 or len(value) > 50:
            raise ValueError("Country cannot exceed 50 characters")
        return value

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )


# -------------------------------------------------- Create user payment method --------------------------------------------------


class UserPaymentMethodBase(BaseModel):
    payment_type: str
    provider: str
    account_number: str
    expiry_date: Optional[date] = None
    is_default: bool = False

    @field_validator("payment_type")
    def validate_payment_type(cls, value: str) -> str:
        # Get all valid enum values
        valid_values = [enum.value for enum in PaymentType]

        # Check if the string matches any enum value
        if value not in valid_values:
            raise ValueError(
                f"Invalid payment type '{value}'. Must be one of: {valid_values}"
            )
        return value  # Return the validated string

    @field_validator("provider")
    def validate_provider(cls, value):
        if len(value) < 1 or len(value) > 50:
            raise ValueError("Provider cannot exceed 50 characters")
        return value

    @field_validator("account_number")
    def validate_account_number(cls, value):
        if len(value) < 1 or len(value) > 100:
            raise ValueError("Account number cannot exceed 100 characters")
        return value

    @field_validator("expiry_date")
    def validate_expiry_date(cls, value):
        if value and value < date_now():
            raise ValueError("Expiry date must be in the future")
        return value

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )


class UserPaymentMethodResponse(BaseModel):
    id: int
    user_id: int
    payment_type: str
    provider: str
    account_number: str
    created_at: datetime
    updated_at: datetime

    @field_validator("account_number")
    def validate_account_number(cls, value):
        # censor account number
        return value[:4] + "*" * (len(value) - 4)

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )
