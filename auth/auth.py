from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from repo.user import user_by_id_repo


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = user_by_id_repo(user_id)
        if not user or not user.is_admin:
            return jsonify({"error": "Admin access required"}), 403
        return fn(*args, **kwargs)

    return wrapper