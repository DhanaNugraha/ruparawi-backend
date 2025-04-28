from datetime import datetime
import re
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator


class VendorCreateRequest(BaseModel):
    business_name: str 
    business_email: str
    business_phone: str 
    business_address: str 
    business_description: Optional[str] = None
    business_logo_url: Optional[str] = None

    @field_validator("business_name")
    def validate_business_name(cls, value):
        if len(value) < 2 or len(value) > 100:
            raise ValueError("Business name must be between 2 and 100 characters")
        
        return value
    
    @field_validator("business_email")
    def validate_email(cls, value):
        if not value:
            raise ValueError("Email cannot be empty")

        # Basic email regex pattern
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

        if not re.fullmatch(pattern, value):
            raise ValueError("Invalid email format")

        # Additional checks
        if ".." in value:
            raise ValueError("Invalid email: consecutive dots")

        if len(value.split("@")[0]) > 64:
            raise ValueError("Email username too long (max 64 chars)")

        return value.lower()  # Normalize to lowercase
    
    @field_validator("business_phone")
    def validate_phone(cls, value):
        if not value:
            raise ValueError("Phone number cannot be empty")
        
        pattern = r"^\+?[0-9\s\-]{10,15}$"

        if not re.fullmatch(pattern, value):
            raise ValueError("Invalid phone number format")
        
        return value
    
    @field_validator("business_address")
    def validate_address(cls, value):
        if len(value) < 5 or len(value) > 200:
            raise ValueError("Business address must be between 5 and 200 characters")
        
        return value
    

    @field_validator("business_description")
    def validate_description(cls, value):
        if value and len(value) > 500:
            raise ValueError("Description cannot exceed 500 characters")
        
        return value
    
    @field_validator("business_logo_url")
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

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )


class VendorProfileResponse(BaseModel):
    business_name: str
    business_email: str
    business_phone: str
    business_address: str
    business_description: Optional[str] = None
    business_logo_url: Optional[str] = None
    vendor_status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )