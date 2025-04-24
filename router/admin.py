from flask import Blueprint, request
from flask_jwt_extended import current_user, jwt_required
from auth.auth import super_admin_required, admin_required
from repo.user import log_admin_action_repo


admin_router = Blueprint("admin_router", __name__, url_prefix="/admin")

# add category will be any admin

# delete user permanently will require super

# logs admin actions after every request
@admin_router.after_request
def log_admin_actions_after_request(response):
    if request.method in ["PUT", "DELETE", "POST"]:
        log_admin_action_repo(current_user, request)
        return response
