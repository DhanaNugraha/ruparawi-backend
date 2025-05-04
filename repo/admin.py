from datetime import timezone
from instance.database import db
from models.product import Product, ProductCategory, Promotion
from models.user import AdminLog, User
from models.article import Article
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


def get_admin_logs_repo():
    return db.paginate(db.select(AdminLog))


# ------------------ CATEGORY -----------------


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


# ------------------ ARTICLE ------------------


def create_article_repo(title, content, author_id):
    article = Article(title=title, content=content, author_id=author_id)
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


# ------------------ Promotions ------------------


def create_promotion_repo(admin_id, promotion_data):
    promotion = Promotion(
        title=promotion_data.title,
        description=promotion_data.description,
        promo_code=promotion_data.promo_code,
        discount_value=promotion_data.discount_value,
        promotion_type=promotion_data.promotion_type,
        start_date=promotion_data.start_date,
        end_date=promotion_data.end_date,
        admin_id=admin_id,
        image_url=promotion_data.image_url,
        max_discount=promotion_data.max_discount,
        usage_limit=promotion_data.usage_limit,
    )

    db.session.add(promotion)
    db.session.flush()
    return promotion


def update_promotion_repo(promotion_id, update_data):
    promotion = db.one_or_404(db.select(Promotion).filter_by(id=promotion_id))

    for key, value in update_data.model_dump().items():
        if value is not None:
            setattr(promotion, key, value)

    db.session.flush()
    return promotion


def add_products_to_promotion_repo(promotion, product_ids_list):
    for product_id in product_ids_list:
        product = db.one_or_404(db.select(Product).filter_by(id=product_id), description=f"Product does not exist '{product_id}'.")

        promotion.products.append(product)

def add_categories_to_promotion_repo(promotion, category_name_list):
    for category_name in category_name_list:
        category = db.one_or_404(
            db.select(ProductCategory).filter_by(name=category_name),
            description=f"Category does not exist '{category_name}'.",
        )

        promotion.categories.append(category)


def get_promotion_detail_repo(promotion_id):
    return db.one_or_404(db.select(Promotion).filter_by(id=promotion_id))


def list_active_promotions_repo():
    now_ = now()
    return (
        db.paginate(
            db.select(Promotion)
            .filter(
                Promotion.start_date <= now_, Promotion.end_date >= now_
            )
            .order_by(Promotion.end_date)
        )
    )


def list_all_promotions_repo():
    return db.paginate(db.select(Promotion).order_by(Promotion.end_date))


def get_promotion_by_id_repo(promotion_id):
    return db.one_or_404(db.select(Promotion).filter_by(id=promotion_id))