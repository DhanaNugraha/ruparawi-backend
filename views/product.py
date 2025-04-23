from flask import jsonify
from pydantic import ValidationError
from instance.database import db
from repo.product import (
    create_product_repo,
    get_product_detail_repo,
    get_products_list_repo,
    process_sustainability_repo,
    process_tags_repo,
    soft_delete_product_repo,
    update_product_repo,
)
from schemas.product import (
    ProductCreateRequest,
    ProductCreatedResponse,
    ProductDeleteResponse,
    ProductDetailResponse,
    ProductListFilters,
    ProductListResponse,
    ProductUpdateRequest,
)


# ------------------------------------------------------ Create Product --------------------------------------------------


def create_product_view(user, product_request):
    if not user.is_vendor:
        return jsonify(
            {
                "message": "User is not a vendor",
                "success": False,
                "location": "view create product vendor validation",
            }
        ), 403

    try:
        product_data_validated = ProductCreateRequest.model_validate(product_request)

        # flush product and get product id
        product = create_product_repo(product_data_validated, user.id)

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

        # serialize data
        products_response = [
            ProductListResponse.model_validate(product).model_dump()
            for product in paginated_product.items
        ]

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
        )

    except ValidationError as e:
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view list products request validation",
            }
        ), 400

    except Exception as e:
        return jsonify(
            {"message": str(e), "success": False, "location": "view list products repo"}
        ), 500


# ------------------------------------------------------ Get Product Detail --------------------------------------------------


def get_product_detail_view(product_id):
    try:
        product = get_product_detail_repo(product_id)

        serialized_product = ProductDetailResponse.model_validate(product).model_dump()

        return jsonify({"success": True, "product": serialized_product}), 200

    except ValidationError as e:
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view get product detail data validation",
            }
        ), 500

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
