from flask import jsonify
from pydantic import ValidationError
from instance.database import db
from models.user import UserRole
from repo.vendor import vendor_register_repo
from schemas.vendor import VendorCreateRequest


def vendor_register_view(user, vendor_request):
    try:
        # Prevent duplicate applications
        if user.role == UserRole.VENDOR.value:
            return jsonify(
                {"error": "Vendor already registered", "status": user.vendor_status}
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
