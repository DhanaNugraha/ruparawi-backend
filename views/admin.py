from flask import jsonify
from flask_jwt_extended import current_user
from models.articles import Article
from pydantic import ValidationError
from instance.database import db
from models.user import VendorStatus
from repo.admin import (
  check_parent_category_repo, 
  create_article_repo, 
  create_category_repo, 
  get_article_by_id_repo, 
  soft_delete_category_repo, 
  update_category_repo,
  get_admin_logs_repo,
  update_category_repo,
from repo.vendor import (
    get_vendors_repo,
    process_vendor_application_repo,
    vendor_profile_by_user_id_repo,
)
from schemas.admin import (
    AdminLogsResponse,
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
    CategoryUpdateResponse,
    VendorApprovalRequest,
)
from schemas.vendor import VendorProfileResponse


# ------------------------------------------------------ Create Category --------------------------------------------------


def create_category_view(category_request):
    try:
        category_data_validated = CategoryCreate.model_validate(category_request)

        # subcategory path
        if category_data_validated.parent_category_id:
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


# ------------------------------------------------------ Get all vendors ---------------------------------------------------


def get_vendors_view():
    try:
        pending_vendors, approved_vendors, rejected_vendors = get_vendors_repo()

        # pagination
        total_vendors = (
            pending_vendors.total + approved_vendors.total + rejected_vendors.total
        )

        pages = max(
            pending_vendors.pages, approved_vendors.pages, rejected_vendors.pages
        )

        current_page = max(
            pending_vendors.page, approved_vendors.page, rejected_vendors.page
        )

        per_page = max(
            pending_vendors.per_page,
            approved_vendors.per_page,
            rejected_vendors.per_page,
        )

        # responses
        pending_vendors_response = [
            VendorProfileResponse.model_validate(vendor).model_dump()
            for vendor in pending_vendors.items
        ]

        approved_vendors_response = [
            VendorProfileResponse.model_validate(vendor).model_dump()
            for vendor in approved_vendors.items
        ]

        rejected_vendors_response = [
            VendorProfileResponse.model_validate(vendor).model_dump()
            for vendor in rejected_vendors.items
        ]

        return jsonify(
            {
                "pagination": {
                    "total": total_vendors,
                    "pages": pages,
                    "current_page": current_page,
                    "per_page": per_page,
                },
                "success": True,
                "message": "Vendors fetched successfully",
                "vendors": {
                    "pending": pending_vendors_response,
                    "approved": approved_vendors_response,
                    "rejected": rejected_vendors_response,
                },
            }
        ), 200

    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view get pending vendors repo",
            }
        ), 500


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


# ------------------------------------------------------ Get admin logs ---------------------------------------------------


def get_admin_logs_view():
    try:
        logs = get_admin_logs_repo()

        logs_response = [
            AdminLogsResponse.model_validate(log).model_dump() for log in logs.items
        ]

        return jsonify(
            {
                "pagination": {
                    "total": logs.total,
                    "pages": logs.pages,
                    "current_page": logs.page,
                    "per_page": logs.per_page,
                },
                "success": True,
                "message": "Admin logs fetched successfully",
                "logs": logs_response,
            }
        ), 200

    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view get admin logs repo",
            }
        ), 500

  
 # ------------------------------------------------------ Management Article --------------------------------------------------

def create_article_view(data):
    try:
        title = data.get("title")
        content = data.get("content")

        if not title or not content:
            return jsonify({
                "success": False,
                "message": "Title and content are required",
                "location": "view create article validation"
            }), 400
        
        if len(title) > 255:
            return jsonify({
                "success": False,
                "message": "Title must be less than 255 characters",
                "location": "view create article validation"
            }), 400

        if len(content) < 500:
            return jsonify({
                "success": False,
                "message": "Content must be at least 500 characters",
                "location": "view create article validation"
            }), 400

        if len(content) > 20000:
            return jsonify({
                "success": False,
                "message": "Content must be less than 20000 characters",
                "location": "view create article validation"
            }), 400
        
        new_article = create_article_repo(title, content, current_user.id)

        return jsonify({
            "success": True,
            "message": "Article created successfully",
            "article": {
                "id": new_article.id,
                "title": new_article.title,
                "content": new_article.content,
                "author_id": new_article.author_id,
                "created_at": new_article.created_at.isoformat(),
                "updated_at": new_article.updated_at.isoformat()
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": str(e),
            "location": "view create article repo"
        }), 500


def get_articles_view():
    try:
        articles = Article.query.all()
        result = [
            {
                "id": article.id,
                "title": article.title,
                "content": article.content,
                "author_id": article.author_id,
                "created_at": article.created_at.isoformat(),
                "updated_at": article.updated_at.isoformat()
            }
            for article in articles
        ]
        return jsonify({
            "success": True,
            "message": "Articles retrieved successfully",
            "articles": result
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e),
            "location": "view get articles repo"
        }), 500


def get_article_by_id_view(article_id):
    try:
        article = get_article_by_id_repo(article_id)

        result = {
            "id": article.id,
            "title": article.title,
            "content": article.content,
            "author_id": article.author_id,
            "created_at": article.created_at.isoformat(),
            "updated_at": article.updated_at.isoformat()
        }

        return jsonify({
            "success": True,
            "message": "Article retrieved successfully",
            "article": result
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e),
            "location": "view get article by id"
        }), 500


def update_article_view(data, article_id):
    try:
        article = Article.query.get(article_id)
        if not article:
            return jsonify({
                "success": False,
                "message": "Article not found",
                "location": "view update article validation"
            }), 404

        title = data.get("title")
        content = data.get("content")

        if title:
            if len(title) > 255:
                return jsonify({
                    "success": False,
                    "message": "Title must be less than 255 characters",
                    "location": "view update article validation"
                }), 400
            article.title = title

        if content:
            if len(content) < 500:
                return jsonify({
                    "success": False,
                    "message": "Content must be at least 500 characters",
                    "location": "view update article validation"
                }), 400
            if len(content) > 20000:
                return jsonify({
                    "success": False,
                    "message": "Content must be less than 20000 characters",
                    "location": "view update article validation"
                }), 400
            article.content = content

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Article updated successfully",
            "article": {
                "id": article.id,
                "title": article.title,
                "content": article.content,
                "author_id": article.author_id,
                "created_at": article.created_at.isoformat(),
                "updated_at": article.updated_at.isoformat()
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": str(e),
            "location": "view update article repo"
        }), 500


def delete_article_view(article_id):
    try:
        article = Article.query.get(article_id)
        if not article:
            return jsonify({
                "success": False,
                "message": "Article not found",
                "location": "view delete article validation"
            }), 404

        db.session.delete(article)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Article deleted successfully"
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": str(e),
            "location": "view delete article repo"
        }), 500


