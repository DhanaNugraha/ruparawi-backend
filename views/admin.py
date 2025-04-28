from flask import jsonify
from flask_jwt_extended import current_user
from models.article import Article
from pydantic import ValidationError
from instance.database import db
from repo.admin import check_parent_category_repo, create_category_repo, get_article_by_id_repo, soft_delete_category_repo, update_category_repo, get_all_articles_repo
from schemas.admin import CategoryCreate, CategoryResponse, CategoryUpdate, CategoryUpdateResponse

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

        return jsonify({
            "success": True,
            "message": "Category created successfully",
            "category": CategoryResponse.model_validate(
                category_data_validated
            ).model_dump(),
        }), 201

    except ValidationError as e:
        return jsonify({
            "message": str(e),
            "success": False,
            "location": "view create category request validation",
        }), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "message": str(e),
            "success": False,
            "location": "view create category repo",
        }), 500


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

        return jsonify({
            "success": True,
            "message": "Category updated successfully",
            "category": CategoryUpdateResponse.model_validate(
                category_data_validated).model_dump(),
        }), 200

    except ValidationError as e:
        return jsonify({
            "message": str(e),
            "success": False,
            "location": "view update category request validation",
        }), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "message": str(e),
            "success": False,
            "location": "view update category repo",
        }), 500
    

# ------------------------------------------------------ Delete category --------------------------------------------------

def soft_delete_category_view(category_id):
    try:
        soft_delete_category_tree(category_id)

        return jsonify({
            "success": True,
            "message": "Category tree soft deleted (archived) successfully",
            
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "message": str(e),
            "success": False,
            "location": "view soft delete category repo",
        }), 500
    

def soft_delete_category_tree(category_id):
    # Recursively soft delete category tree structure
    category = soft_delete_category_repo(category_id)

    # soft delete its sub categories as well
    if category.subcategories:
        for sub_category in category.subcategories:
            soft_delete_category_tree(sub_category.id) 


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
        
        new_article = Article(
            title=title,
            content=content,
            author_id=current_user.id
        )

        db.session.add(new_article)
        db.session.commit()

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
