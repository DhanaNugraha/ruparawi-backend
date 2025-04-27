import re
from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime

# -------------------------------------------------- Register User --------------------------------------------------


class PublicUserProfileResponse(BaseModel):
    id: int
    username: str
    first_name: str | None
    last_name: str | None
    profile_image_url: str | None
    bio: str | None
    role: str
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

    model_config = ConfigDict(
        from_attributes=True,  # Can read SQLAlchemy model
        extra="ignore",  # ignore extra fields
    )
