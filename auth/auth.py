from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from models.user import VendorStatus
from repo.admin import admin_by_id_repo
from repo.vendor import vendor_profile_by_user_id_repo


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            user_id = get_jwt_identity()

            admin = admin_by_id_repo(user_id)

            if not admin:
                return jsonify({"error": "Admin privileges required"}), 403

            else:
                return fn(*args, **kwargs)

        return decorator

    return wrapper


def vendor_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        vendor_profile = vendor_profile_by_user_id_repo(user_id)

        if vendor_profile.vendor_status != VendorStatus.APPROVED.value:
            return jsonify(
                {
                    "message": "Vendor not approved",
                    "status": vendor_profile.vendor_status,
                    "success": False,
                }
            ), 403

        return fn(*args, **kwargs)

    return wrapper
