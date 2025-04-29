from instance.database import db
from models.product import ProductCategory
from models.user import AdminLog, User
from models.articles import Article
from repo.product import get_category_by_id_repo
from shared.time import now, datetime_from_string


def admin_by_id_repo(user_id):
    user = db.session.execute(
        db.select(User).filter_by(id=user_id)
    ).scalar_one_or_none()

    # if user exist and is an admin
    if user and user.admin_profile:
        return user.admin_profile

    else:
        return None


def log_admin_action_repo(user, request):
    log = AdminLog(
        admin_id=user.id,
        action=f"{request.method} {request.path}",
        timestamp=datetime_from_string(str(now())),
    )

    db.session.add(log)
    db.session.commit()


def check_parent_category_repo(category_id):
    return db.one_or_404(
        db.select(ProductCategory).filter_by(id=category_id),
        description=f"Parent category does not exist '{category_id}'.",
    )


def create_category_repo(category_data):
    category = ProductCategory(
        name=category_data.name,
        description=category_data.description,
        parent_category_id=category_data.parent_category_id,
        is_active=True,
    )

    db.session.add(category)
    db.session.commit()

    return category


def update_category_repo(category_id, category_data):
    category = get_category_by_id_repo(category_id)

    if category_data.name:
        category.name = category_data.name

    if category_data.description:
        category.description = category_data.description

    if category_data.parent_category_id:
        category.parent_category_id = category_data.parent_category_id

    db.session.commit()


def soft_delete_category_repo(category_id):
    category = get_category_by_id_repo(category_id)

    category.is_active = False

    # parent category none to prevent being queried in get tree
    category.parent_category_id = None

    db.session.commit()
    return category


def create_article_repo(title, content, author_id):
    article = Article(
        title=title,
        content=content,
        author_id=author_id
    )
    db.session.add(article)
    db.session.commit()
    return article

  
def get_article_by_id_repo(article_id):
    try:
        article = Article.query.get(article_id)
        if not article:
            raise Exception(f"Article with ID {article_id} not found.")
        return article
    except Exception as e:
        raise Exception(f"Error while fetching article by ID: {str(e)}")

        
def get_admin_logs_repo():
    return db.paginate(db.select(AdminLog))

