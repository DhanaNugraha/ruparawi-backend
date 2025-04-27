from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from repo.admin import admin_by_id_repo
from repo.user import user_by_id_repo


def super_admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            user_id = get_jwt_identity()

            admin = admin_by_id_repo(user_id)

            if not admin:
                return jsonify({"error": "Admin privileges required"}), 403
            
            elif admin.access_level != "super":
                return jsonify({"error": "Super admin required"}), 403

            else:
                return fn(*args, **kwargs)

        return decorator

    return wrapper


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


# def vendor_approved_required(fn):
#     @wraps(fn)
#     def wrapper(*args, **kwargs):
#         user_id = get_jwt_identity()
#         user = user_by_id_repo(user_id)

#         if not user or not user.is_vendor:
#             return jsonify({"error": "Vendor account required"}), 403

#         if user.vendor_status != VendorStatus.APPROVED:
#             return jsonify(
#                 {"error": "Vendor not approved", "status": user.vendor_status.value}
#             ), 403

#         return fn(*args, **kwargs)

#     return wrapper