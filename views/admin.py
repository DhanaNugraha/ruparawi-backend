from flask import jsonify
from pydantic import ValidationError
from instance.database import db
from models.user import VendorStatus
from repo.admin import (
    check_parent_category_repo,
    create_category_repo,
    soft_delete_category_repo,
    update_category_repo,
)
from repo.vendor import process_vendor_application_repo, vendor_profile_by_user_id_repo
from schemas.admin import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
    CategoryUpdateResponse,
    VendorApprovalRequest,
)

# ------------------------------------------------------ Create Category --------------------------------------------------


def create_category_view(category_request):
    try:
        category_data_validated = CategoryCreate.model_validate(category_request)

        # subcategory path
        if category_data_validated.parent_category_id:
            # test if it returns 404---------------
            check_parent_category_repo(category_data_validated.parent_category_id)

        # make category
        create_category_repo(category_data_validated)

        return jsonify(
            {
                "success": True,
                "message": "Category created successfully",
                "category": CategoryResponse.model_validate(
                    category_data_validated
                ).model_dump(),
            }
        ), 201

    except ValidationError as e:
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view create category request validation",
            }
        ), 400

    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view create category repo",
            }
        ), 500


# ------------------------------------------------------ Update category --------------------------------------------------


def update_category_view(category_request, category_id):
    try:
        category_data_validated = CategoryUpdate.model_validate(category_request)

        # check if parent exist
        if category_data_validated.parent_category_id:
            # test if it returns 404---------------
            check_parent_category_repo(category_data_validated.parent_category_id)

        # update category
        update_category_repo(category_id, category_data_validated)

        return jsonify(
            {
                "success": True,
                "message": "Category updated successfully",
                "category": CategoryUpdateResponse.model_validate(
                    category_data_validated
                ).model_dump(),
            }
        ), 200

    except ValidationError as e:
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view update category request validation",
            }
        ), 400

    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view update category repo",
            }
        ), 500


# ------------------------------------------------------ Delete category --------------------------------------------------


def soft_delete_category_view(category_id):
    try:
        soft_delete_category_tree(category_id)

        return jsonify(
            {
                "success": True,
                "message": "Category tree soft deleted (archived) successfully",
            }
        ), 200

    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view soft delete category repo",
            }
        ), 500


def soft_delete_category_tree(category_id):
    # Recursively soft delete category tree structure
    category = soft_delete_category_repo(category_id)

    # soft delete its sub categories as well
    if category.subcategories:
        for sub_category in category.subcategories:
            soft_delete_category_tree(sub_category.id)


# ------------------------------------------------------ Review Vendor Application --------------------------------------------------


def review_vendor_application_view(user_id, review_request):
    try:
        review_request_validated = VendorApprovalRequest.model_validate(review_request)

        vendor_profile = vendor_profile_by_user_id_repo(user_id)

        if vendor_profile.vendor_status != VendorStatus.PENDING.value:
            return jsonify(
                {
                    "success": False,
                    "message": "Vendor already approved or rejected",
                }
            ), 400

        process_vendor_application_repo(vendor_profile, review_request_validated)

        # add email notif later for the reject or approve reason

        return jsonify(
            {
                "success": True,
                "message": "Vendor application reviewed successfully",
                "action": f"{review_request_validated.action}",
            }
        ), 200

    except ValidationError as e:
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view review vendor application request validation",
            }
        ), 400

    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view review vendor application repo",
            }
        ), 500
