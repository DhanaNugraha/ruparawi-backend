from .auth import auth_router
from .user import user_router
from .product import products_router
from .admin import admin_router
from .vendor import vendor_router
from .order import order_router

__all__ = ["auth_router", "user_router", "products_router", "admin_router", "vendor_router", "order_router"]