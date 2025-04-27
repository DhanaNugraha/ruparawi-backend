from flask import Blueprint, request
from flask_jwt_extended import current_user, jwt_required
from auth.auth import super_admin_required, admin_required
from repo.admin import log_admin_action_repo
from views.admin import create_category_view, soft_delete_category_view, update_category_view


admin_router = Blueprint("admin_router", __name__, url_prefix="/admin")


@admin_router.route("/category", methods=["POST"])
@jwt_required()
@admin_required()
def create_category():
    return create_category_view(request.json)
        

@admin_router.route(
    "/category/<int:category_id>", methods=["PUT", "DELETE"]
)
@jwt_required()
@admin_required()
def category_detail(category_id):
    match request.method.lower():
        case "put":
            return update_category_view(request.json, category_id)
        
        case "delete":
            return soft_delete_category_view(category_id)



# delete user permanently will require super

# logs admin actions after every request
@admin_router.after_request
@jwt_required()
def log_admin_actions_after_request(response):
    print("Logging admin actions")
    if request.method in ["PUT", "DELETE", "POST"]:
        log_admin_action_repo(current_user, request)

    return response


