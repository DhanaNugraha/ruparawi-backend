from functools import wraps
from flask_jwt_extended import get_jwt_identity
from repo.user import admin_by_id_repo


def super_admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            user_id = get_jwt_identity()

            admin = admin_by_id_repo(user_id)

            if not admin:
                return {"error": "Admin privileges required"}, 403
            
            elif admin.access_level != "super":
                return {"error": "Super admin required"}, 403

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
                return {"error": "Admin privileges required"}, 403

            else:
                return fn(*args, **kwargs)

        return decorator

    return wrapper