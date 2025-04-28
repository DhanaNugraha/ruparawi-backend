from flask import Blueprint, jsonify, request
from flask_jwt_extended import current_user, jwt_required
from jsonschema import ValidationError
from auth.auth import super_admin_required, admin_required
from conftest import db
from repo.admin import log_admin_action_repo
from views.admin import create_article_view, create_category_view, delete_article_view, get_article_by_id_view, get_articles_view, soft_delete_category_view, update_article_view, update_category_view
from models.articles import Article 
from schemas.article import ArticleCreate

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
    if request.method in ["PUT", "DELETE", "POST"]:
        log_admin_action_repo(current_user, request)

    return response


# ------------------------------------------------------ Management Article --------------------------------------------------
@admin_router.route("/article", methods=["POST"])
@jwt_required()
@admin_required()
def create_article():
    try:
        payload = request.get_json()
        validated_data = ArticleCreate(**payload)

        article = Article(
            title=validated_data.title,
            content=validated_data.content,
            author_id=current_user.id

        )
        db.session.add(article)
        db.session.commit()

        return jsonify({"message": "Article created successfully!"}), 201

    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@admin_router.route("/article", methods=["GET"])
@jwt_required()
@admin_required()
def get_articles():
    return get_articles_view()

@admin_router.route("/article/<int:article_id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
@admin_required()
def article_detail(article_id):
    match request.method.lower():
        case "get":
            return get_article_by_id_view(article_id)
        case "put":
            return update_article_view(request.json, article_id)
        case "delete":
            return delete_article_view(article_id)
