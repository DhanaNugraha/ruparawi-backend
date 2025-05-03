from flask import jsonify
from pydantic import ValidationError
from instance.database import db
from repo.admin import get_promotion_by_id_repo, list_active_promotions_repo
from repo.product import (
    add_product_to_wishlist_by_user_id_repo,
    create_product_repo,
    get_category_by_id_repo,
    get_product_detail_repo,
    get_product_primary_image_repo,
    get_products_list_repo,
    get_top_level_categories_repo,
    get_wishlist_by_user_id_repo,
    process_product_images_repo,
    process_sustainability_repo,
    process_tags_repo,
    remove_product_from_wishlist_repo,
    soft_delete_product_repo,
    update_product_repo,
    update_product_image_repo,
)
from schemas.admin import CategoryResponse, CategoryTreeResponse
from schemas.product import (
    ProductCreateRequest,
    ProductCreatedResponse,
    ProductDeleteResponse,
    ProductDetailResponse,
    ProductListFilters,
    ProductListResponse,
    ProductUpdateRequest,
    PromotionDetailResponse,
    PromotionListResponse,
    WishlistProductResponse,
    WishlistResponse,
)


# ------------------------------------------------------ Create Product --------------------------------------------------


def create_product_view(user, product_request):
    try:
        product_data_validated = ProductCreateRequest.model_validate(product_request)

        # flush product and get product id
        product = create_product_repo(product_data_validated, user.id)

        # add product images to images table
        process_product_images_repo(
            product_data_validated.primary_image_url,
            product_data_validated.images,
            product.id,
        )

        # add new tags to tags table and append relationship of product to association table
        process_tags_repo(product_data_validated.tags, product)

        # add new sus attrs to sus_attrs table and append relationship of product to association table
        process_sustainability_repo(
            product_data_validated.sustainability_attributes, product
        )

        db.session.commit()

        return jsonify(
            {
                "message": "Product created successfully",
                "product": ProductCreatedResponse.model_validate(product).model_dump(),
                "success": True,
            }
        ), 201

    except ValidationError as e:
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view create product request validation",
            }
        ), 400

    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view create product repo",
            }
        ), 500


# ------------------------------------------------------ Get Products List --------------------------------------------------


def list_products_view(request_args):
    try:
        filtered_products_data_validated = ProductListFilters.model_validate(
            request_args.to_dict(flat=False)
        )

        paginated_product = get_products_list_repo(
            filtered_products_data_validated, request_args
        )

        products_response = []

        for product in paginated_product.items:
            # update rating stats
            product.update_rating_stats()

            # serialize data
            products_response.append(
                ProductListResponse(
                    primary_image_url=[image.image_url for image in product.images if image.is_primary],
                    id=product.id,
                    name=product.name,
                    price=product.price,
                    category_id=product.category_id,
                    tags=product.tags,
                    vendor_id=product.vendor_id,
                    review_count=product.review_count,
                    average_rating=product.average_rating,
                ).model_dump()
            )

        return jsonify(
            {
                "success": True,
                "products": products_response,
                "pagination": {
                    "total": paginated_product.total,
                    "pages": paginated_product.pages,
                    "current_page": paginated_product.page,
                    "per_page": paginated_product.per_page,
                },
            }
        ), 200

    except ValidationError as e:
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view list products request validation",
            }
        ), 400

    except Exception as e:
        db.session.rollback()
        return jsonify(
            {"message": str(e), "success": False, "location": "view list products repo"}
        ), 500


# ------------------------------------------------------ Get Product Detail --------------------------------------------------


def get_product_detail_view(product_id):
    try:
        product = get_product_detail_repo(product_id)

        # update_rating
        product.update_rating_stats()

        serialized_product = ProductDetailResponse.model_validate(
            product
        ).model_dump()

        return jsonify({"success": True, "product": serialized_product}), 200

    except Exception as e:
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view get product detail repo",
            }
        ), 500


# ------------------------------------------------------ Update Product --------------------------------------------------


def update_product_view(user, update_request, product_id):
    try:
        # validate data
        update_data_validated = ProductUpdateRequest.model_validate(update_request)

        # update product and get the product
        product = update_product_repo(user.id, product_id, update_data_validated)

        if update_data_validated.tags:
            # clear existing tags
            product.tags.clear()

            # add new tags to tags table and append relationship of product to association table
            process_tags_repo(update_data_validated.tags, product)

        if update_data_validated.sustainability_attributes:
            # clear existing sustainability attributes
            product.sustainability_attributes.clear()

            # add new sus attrs to sus_attrs table and append relationship of product to association table
            process_sustainability_repo(
                update_data_validated.sustainability_attributes, product
            )

        if update_data_validated.images or update_data_validated.primary_image_url:
            update_product_image_repo(
                product, update_data_validated.primary_image_url, update_data_validated.images
            )


        db.session.commit()

        return jsonify(
            {
                "message": "Product updated successfully",
                "product": ProductDetailResponse.model_validate(product).model_dump(),
                "success": True,
            }
        ), 200

    except ValidationError as e:
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view update product request validation",
            }
        ), 400

    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view update product repo",
            }
        ), 500


# ------------------------------------------------------ Delete Product --------------------------------------------------


# soft delete (archive)
def soft_delete_product_view(user, product_id):
    try:
        # get product
        product = get_product_detail_repo(product_id)

        if product.vendor_id != user.id:
            return jsonify(
                {
                    "message": "You are not authorized to delete this product",
                    "success": False,
                }
            ), 403

        soft_delete_product_repo(product)

        return jsonify(
            {
                "message": "Product soft deleted (archived) successfully",
                "product": ProductDeleteResponse.model_validate(product).model_dump(),
                "success": True,
            }
        ), 200

    except ValidationError as e:
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view delete product request validation",
            }
        ), 400

    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view delete product repo",
            }
        ), 500


# ------------------------------------------------------ Add product to wishlist --------------------------------------------------


def add_product_to_wishlist_view(user, product_id):
    try:
        # get product
        product = get_product_detail_repo(product_id)

        wishlist = add_product_to_wishlist_by_user_id_repo(user.id, product)

        if wishlist is None:
            return jsonify(
                {
                    "message": "Product already in wishlist",
                    "success": False,
                }
            ), 404

        return jsonify(
            {
                "message": f"{product.name} added to wishlist successfully",
                "success": True,
            }
        ), 200

    except ValidationError as e:
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view add product to wishlist request validation",
            }
        ), 400

    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view add product to wishlist repo",
            }
        ), 500


# ------------------------------------------------------ Remove product from wishlist --------------------------------------------------


def remove_product_from_wishlist_view(user, product_id):
    try:
        # get product
        product = get_product_detail_repo(product_id)

        wishlist = get_wishlist_by_user_id_repo(user.id)

        updated_wishlist = remove_product_from_wishlist_repo(wishlist, product)

        if updated_wishlist is None:
            return jsonify(
                {
                    "message": "Product not in wishlist",
                    "success": False,
                }
            ), 404

        return jsonify(
            {
                "message": "Product removed from wishlist successfully",
                "success": True,
            }
        ), 200

    except ValidationError as e:
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view remove product from wishlist request validation",
            }
        ), 400

    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view remove product from wishlist repo",
            }
        ), 500


# ------------------------------------------------------ Get wishlist --------------------------------------------------


def get_wishlist_view(user):
    try:
        wishlist = get_wishlist_by_user_id_repo(user.id)

        wishlist_product_response = []

        for product in wishlist.products.all():
            primary_image = get_product_primary_image_repo(product.id)

            wishlist_product_response.append(
                WishlistProductResponse(
                    primary_image=primary_image,
                    **ProductDetailResponse.model_validate(product).model_dump(),
                )
            )

        wishlist_response = WishlistResponse(
            products=wishlist_product_response, count=len(wishlist_product_response)
        )

        return {
            "success": True,
            "message": "Wishlist fetched successfully",
            "wishlist": wishlist_response.model_dump(),
        }, 200

    except Exception as e:
        return {
            "message": str(e),
            "success": False,
            "location": "view get wishlist repo",
        }, 500


# ------------------------------------------------------ Get Category Tree --------------------------------------------------


def get_category_tree_view():
    try:
        # active categories with no parents
        top_categories = get_top_level_categories_repo()

        # build category tree
        categories_tree = []

        for category in top_categories:
            categories_tree.append(build_category_tree(category))

        return {
            "success": True,
            "message": "Category tree fetched successfully",
            "data": CategoryTreeResponse(categories=categories_tree).model_dump(),
        }, 200

    except Exception as e:
        return {
            "message": str(e),
            "success": False,
            "location": "view get category tree repo",
        }, 500


def build_category_tree(category):
    # Recursively build category tree structure
    category_data = CategoryResponse.model_validate(category)
    if category.subcategories:
        category_data.subcategories = [
            build_category_tree(sub) for sub in category.subcategories
        ]
    return category_data


# ------------------------------------------------------ Get category detail --------------------------------------------------


def get_category_detail_view(category_id):
    try:
        category = get_category_by_id_repo(category_id)

        return {
            "success": True,
            "message": "Category fetched successfully",
            "category": CategoryResponse.model_validate(category).model_dump(),
        }, 200

    except Exception as e:
        return {
            "message": str(e),
            "success": False,
            "location": "view get category detail repo",
        }, 500



# ------------------------------------------------------ Get promotions --------------------------------------------------


def get_promotions_view():
    try:
        promotions = list_active_promotions_repo()

        promotions_response = [
            PromotionListResponse.model_validate(promotion).model_dump() for promotion in promotions.items
        ]

        return jsonify(
            {
                "pagination": {
                    "total": promotions.total,
                    "pages": promotions.pages,
                    "current_page": promotions.page,
                    "per_page": promotions.per_page,
                },
                "success": True,
                "message": "Promotions fetched successfully",
                "promotions": promotions_response,
            }
        ), 200

    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view get all promotions repo",
            }
        ), 500


# ------------------------------------------------------ Get promotion detail --------------------------------------------------


def get_promotion_detail_view(promotion_id):
    try:
        promotion = get_promotion_by_id_repo(promotion_id)

        return jsonify(
            {
                "success": True,
                "message": "Promotion fetched successfully",
                "promotion": PromotionDetailResponse.model_validate(promotion).model_dump(),
            }
        ), 200

    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view get promotion detail repo",
            }
        ), 500