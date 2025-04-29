from flask import jsonify
from pydantic import ValidationError
from instance.database import db
from models.user import UserRole
from repo.product import get_vendor_products_repo
from repo.vendor import vendor_profile_by_user_id_repo, vendor_register_repo
from schemas.product import VendorProductsResponse
from schemas.vendor import VendorCreateRequest, VendorProfileResponse

# -------------------------------------------------------------- Register Vendor ---------------------------------------------------------------------------


def vendor_register_view(user, vendor_request):
    try:
        # Prevent duplicate applications
        if user.role == UserRole.VENDOR.value:
            vendor_profile = vendor_profile_by_user_id_repo(user.id)

            return jsonify(
                {
                    "message": "Vendor already registered",
                    "status": vendor_profile.vendor_status,
                }
            ), 400

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
        vendor_profile = vendor_profile_by_user_id_repo(user.id)

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
