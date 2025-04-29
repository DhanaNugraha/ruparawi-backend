from pydantic import BaseModel, ConfigDict, field_validator

class ArticleCreate(BaseModel):
    title: str
    content: str

    @field_validator("title")
    def validate_title(cls, value):
        value = value.strip()
        if len(value) < 2 or len(value) > 255:
            raise ValueError("Title must be between 2 and 255 characters")
        
        return value

    @field_validator("content")
    def validate_content(cls, value):
        value = value.strip()
        if len(value) < 500 or len(value) > 20000:
            raise ValueError("Content must be between 500 and 20000 characters")
        
        return value

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore", 
    )