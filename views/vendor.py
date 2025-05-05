from flask import jsonify
from pydantic import ValidationError
from instance.database import db
from repo.product import get_vendor_products_repo
from repo.vendor import get_vendor_recent_orders_repo, get_vendor_stats_repo, update_vendor_profile_repo, vendor_register_repo
from schemas.product import VendorProductsResponse
from schemas.vendor import (
    VendorCreateRequest,
    VendorProfileResponse,
    VendorUpdateRequest,
)

# -------------------------------------------------------------- Register Vendor ---------------------------------------------------------------------------


def vendor_register_view(user, vendor_request):
    try:
        vendor_data_validated = VendorCreateRequest.model_validate(vendor_request)

        vendor_register_repo(user, vendor_data_validated)

        return jsonify(
            {
                "message": f"Vendor {vendor_data_validated.business_name} application submitted for review",
                "status": "pending",
            }
        ), 201

    except ValidationError as e:
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view register vendor request validation",
            }
        ), 400

    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view register vendor repo",
            }
        ), 500


# -------------------------------------------------------------- Get vendor profile ---------------------------------------------------------------------------


def get_vendor_profile_view(user):
    try:
        vendor_profile = user.vendor_profile

        return jsonify(
            {
                "success": True,
                "vendor": VendorProfileResponse.model_validate(
                    vendor_profile
                ).model_dump(),
            }
        ), 200

    except Exception as e:
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view get vendor profile repo",
            }
        ), 500
    

# -------------------------------------------------------------- Update vendor profile ---------------------------------------------------------------------------


def update_vendor_profile_view(user, vendor_request):
    try:
        vendor_data_validated = VendorUpdateRequest.model_validate(vendor_request)

        vendor_profile = user.vendor_profile

        update_vendor_profile_repo(vendor_profile, vendor_data_validated)

        return jsonify(
            {
                "success": True,
                "message": "Profile updated successfully",
                "vendor": VendorProfileResponse.model_validate(
                    user.vendor_profile
                ).model_dump(),
            }
        ), 200

    except ValidationError as e:
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view update vendor profile request validation",
            }
        ), 400

    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view update vendor profile repo",
            }
        ), 500


# -------------------------------------------------------------- Get vendor products ---------------------------------------------------------------------------


def get_vendor_products_view(user):
    try:
        paginated_products = get_vendor_products_repo(user.id)

        products_response = [
            VendorProductsResponse.model_validate(product).model_dump()
            for product in paginated_products.items
        ]

        return jsonify(
            {
                "success": True,
                "products": products_response,
                "pagination": {
                    "total": paginated_products.total,
                    "pages": paginated_products.pages,
                    "current_page": paginated_products.page,
                    "per_page": paginated_products.per_page,
                },
            }
        ), 200

    except Exception as e:
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view get vendor products repo",
            }
        ), 500


# -------------------------------------------------------------- Get vendor stats ---------------------------------------------------------------------------


def get_vendor_stats_view(user):
    try:
        stats = get_vendor_stats_repo(user.id)

        return jsonify(
            {
                "success": True,
                "vendor_stats": stats,
            }
        ), 200

    except Exception as e:
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view get vendor stats repo",
            }
        ), 500
    

# -------------------------------------------------------------- Get vendor recent orders ---------------------------------------------------------------------------


def get_vendor_recent_orders_view(user):
    try:
        recent_orders = get_vendor_recent_orders_repo(user)

        return jsonify(
            {
                "success": True,
                "recent_orders": [
                    {
                        "order_id": order.id,
                        "product": order.product_name,
                        "customer": order.customer_username,
                        "qty": order.quantity,
                        "total": round(float(order.total_price), 2),
                        "order_date": order.created_at,
                        "order_status": order.status,
                    }
                    for order in recent_orders
                ],
            }
        ), 200

    except Exception as e:
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view get vendor recent orders repo",
            }
        ), 500