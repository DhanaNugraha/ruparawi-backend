from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator


class CategoryCreate(BaseModel):
    parent_category_id: Optional[int] = None
    name: str
    description: Optional[str] = None

    @field_validator("name")
    def validate_name(cls, value):
        if len(value) < 2 or len(value) > 50:
            raise ValueError("Name must be between 2 and 50 characters")
        
        return value

    model_config = ConfigDict(from_attributes=True)


class CategoryResponse(BaseModel):
    id: Optional[int] = None
    parent_category_id: Optional[int] = None
    subcategories: Optional[List["CategoryResponse"]] = [] #subcategory is a nested class
    name: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


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

    model_config = ConfigDict(from_attributes=True)

class CategoryUpdateResponse(BaseModel):
    id: Optional[int] = None
    parent_category_id: Optional[int] = None
    name: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
