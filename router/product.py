from flask import Blueprint, request
from flask_jwt_extended import current_user, jwt_required
from auth.auth import vendor_required
from views.product import add_product_to_wishlist_view, create_product_view, get_category_detail_view, get_category_tree_view, get_product_detail_view, get_promotion_detail_view, get_promotions_view, get_wishlist_view, list_products_view, remove_product_from_wishlist_view, soft_delete_product_view, update_product_view


products_router = Blueprint("products_router", __name__, url_prefix="/products")


# ------------------ Vendor Private Path ------------------

# vendor private path
@products_router.route("", methods=["POST"])
@jwt_required()
@vendor_required
def create_product():
    return create_product_view(current_user, request.json)

# vendor private path
@products_router.route("/<int:product_id>", methods=["PUT", "DELETE"])
@jwt_required()
@vendor_required
def specific_product_route(product_id):
    match request.method.lower():
        case "put":
            return update_product_view(current_user, request.json, product_id)
        
        case "delete":
            return soft_delete_product_view(current_user, product_id)


# ------------------ Get products ------------------
 
# public path
@products_router.route("", methods=["GET"])
def list_products():
    return list_products_view(request.args)

# public path
@products_router.route("/<int:product_id>", methods=["GET"])
def get_product_detail(product_id):
    return get_product_detail_view(product_id)


# ------------------ Wishlist ------------------

@products_router.route("/wishlist/<int:product_id>", methods=["POST", "DELETE"])
@jwt_required()
def wishlist(product_id):
    match request.method.lower():
        case "post":
            return add_product_to_wishlist_view(current_user, product_id)
        
        case "delete":
            return remove_product_from_wishlist_view(current_user, product_id)
        
@products_router.route("/wishlist", methods=["GET"])
@jwt_required()
def get_wishlist():
    return get_wishlist_view(current_user)


# ------------------ Category ------------------

# public path
@products_router.route("/category", methods=["GET"])
def get_all_categories():
    return get_category_tree_view()

# public path
@products_router.route("/category/<int:category_id>", methods=["GET"])
def get_category_detail(category_id):
    return get_category_detail_view(category_id)


# ------------------ Promotions ------------------

@products_router.route("/promotions", methods=["GET"])
@jwt_required()
def get_promotions():
    return get_promotions_view()

@products_router.route("/promotions/<int:promotion_id>", methods=["GET"])
@jwt_required()
def get_promotion_detail(promotion_id):
    return get_promotion_detail_view(promotion_id)

    