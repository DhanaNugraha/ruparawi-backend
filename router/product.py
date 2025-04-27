from flask import Blueprint, request
from flask_jwt_extended import current_user, jwt_required
from views.product import create_product_view, get_category_detail_view, get_category_tree_view, get_product_detail_view, list_products_view, soft_delete_product_view, update_product_view


products_router = Blueprint("products_router", __name__, url_prefix="/products")


# vendor private path
@products_router.route("", methods=["POST"])
@jwt_required()
def create_product():
    return create_product_view(current_user, request.json)

# vendor private path
@products_router.route("/<int:product_id>", methods=["PUT", "DELETE"])
@jwt_required()
def specific_product_route(product_id):
    match request.method.lower():
        case "put":
            return update_product_view(current_user, request.json, product_id)
        
        case "delete":
            return soft_delete_product_view(current_user, product_id)

# public path
@products_router.route("", methods=["GET"])
def list_products():
    return list_products_view(request.args)

# public path
@products_router.route("/<int:product_id>", methods=["GET"])
def get_product_detail(product_id):
    return get_product_detail_view(product_id)

# public path
@products_router.route("/category", methods=["GET"])
def get_all_categories():
    return get_category_tree_view()

# public path
@products_router.route("/category/<int:category_id>", methods=["GET"])
def get_category_detail(category_id):
    return get_category_detail_view(category_id)



    