from .auth import auth_router
from .user import user_router
from .product import products_router
from .admin import admin_router

__all__ = ["auth_router", "user_router", "products_router", "admin_router"]