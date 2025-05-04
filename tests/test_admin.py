import models

# uv run pytest -v -s --cov=.
# uv run pytest tests/test_admin.py -v -s --cov=. --cov-report term-missing


# ---------------------------------------------------------------------------- Admin route Test ----------------------------------------------------------------------------


def test_admin_required(client, mock_user_data, mock_token_data, roles_data_inject):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    admin_route = client.post("/admin/category", headers=mock_token_data)

    assert admin_route.status_code == 403


# ---------------------------------------------------------------------------- Create category Tests ----------------------------------------------------------------------------


def test_create_category(
    client,
    mock_user_data,
    mock_token_data,
    mock_category_data,
    db,
    admins_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    create_category = client.post(
        "/admin/category", json=mock_category_data, headers=mock_token_data
    )

    assert create_category.status_code == 201
    assert create_category.json["success"] is True
    assert create_category.json["message"] == "Category created successfully"
    assert create_category.json["category"]["name"] == mock_category_data["name"]

    categories = db.session.execute(db.select(models.ProductCategory)).scalars().all()

    assert len(categories) == 1
    assert categories[0].name == mock_category_data["name"]


def test_create_category_name_validation_error(
    client,
    mock_user_data,
    mock_token_data,
    mock_category_data,
    admins_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_category_data["name"] = ""
    create_category = client.post(
        "/admin/category", json=mock_category_data, headers=mock_token_data
    )

    assert create_category.status_code == 400
    assert create_category.json["success"] is False
    assert create_category.json["location"] == "view create category request validation"


def test_create_subcategory(
    client,
    mock_user_data,
    mock_token_data,
    mock_subcategory_data,
    db,
    admins_data_inject,
    category_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    create_subcategory = client.post(
        "/admin/category", json=mock_subcategory_data, headers=mock_token_data
    )

    assert create_subcategory.status_code == 201
    assert create_subcategory.json["success"] is True
    assert create_subcategory.json["message"] == "Category created successfully"

    categories = db.session.execute(
        db.select(models.ProductCategory).filter_by(parent_category_id=2)
    ).scalar_one_or_none()

    assert categories.name == mock_subcategory_data["name"]


def test_create_subcategory_parent_category_invalid(
    client,
    mock_user_data,
    mock_token_data,
    mock_subcategory_data,
    admins_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    create_subcategory = client.post(
        "/admin/category", json=mock_subcategory_data, headers=mock_token_data
    )

    assert create_subcategory.status_code == 500
    assert create_subcategory.json["success"] is False
    assert create_subcategory.json["location"] == "view create category repo"


# ---------------------------------------------------------------------------- Update category Tests ----------------------------------------------------------------------------


def test_update_category(
    client,
    mock_user_data,
    mock_token_data,
    mock_update_category_data,
    db,
    category_data_inject,
    admins_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    update_category = client.put(
        "/admin/category/1", json=mock_update_category_data, headers=mock_token_data
    )

    assert update_category.status_code == 200
    assert update_category.json["success"] is True
    assert update_category.json["message"] == "Category updated successfully"
    assert update_category.json["category"]["name"] == mock_update_category_data["name"]

    categories = db.session.execute(
        db.select(models.ProductCategory).filter_by(id=1)
    ).scalar_one_or_none()

    assert categories.name == mock_update_category_data["name"]


def test_update_category_validation_error(
    client,
    mock_user_data,
    mock_token_data,
    mock_update_category_data,
    admins_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_update_category_data["name"] = ""

    update_category = client.put(
        "/admin/category/1", json=mock_update_category_data, headers=mock_token_data
    )

    assert update_category.status_code == 400
    assert update_category.json["success"] is False
    assert update_category.json["location"] == "view update category request validation"


def test_update_category_parent_category_invalid(
    client,
    mock_user_data,
    mock_token_data,
    mock_update_category_data,
    db,
    category_data_inject,
    admins_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_update_category_data["parent_category_id"] = 5

    update_category = client.put(
        "/admin/category/1", json=mock_update_category_data, headers=mock_token_data
    )

    assert update_category.status_code == 500
    assert update_category.json["success"] is False
    assert update_category.json["location"] == "view update category repo"


# ---------------------------------------------------------------------------- Delete category Tests ----------------------------------------------------------------------------


def test_delete_category(
    client,
    mock_user_data,
    mock_token_data,
    db,
    category_data_inject,
    admins_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    delete_category = client.delete("/admin/category/1", headers=mock_token_data)

    assert delete_category.status_code == 200
    assert delete_category.json["success"] is True
    assert (
        delete_category.json["message"]
        == "Category tree soft deleted (archived) successfully"
    )

    categories = db.session.execute(
        db.select(models.ProductCategory).filter_by(id=1)
    ).scalar_one_or_none()

    assert categories.is_active is False


def test_delete_category_tree(
    client,
    mock_category_data,
    mock_subcategory_data,
    mock_user_data,
    mock_token_data,
    admins_data_inject,
    db,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    create_category = client.post(
        "/admin/category", json=mock_category_data, headers=mock_token_data
    )

    assert create_category.status_code == 201

    mock_subcategory_data["parent_category_id"] = 1

    create_subcategory = client.post(
        "/admin/category", json=mock_subcategory_data, headers=mock_token_data
    )

    assert create_subcategory.status_code == 201

    delete_category = client.delete("/admin/category/1", headers=mock_token_data)

    assert delete_category.status_code == 200

    categories = (
        db.session.execute(db.select(models.ProductCategory).filter_by(is_active=False))
        .scalars()
        .all()
    )

    assert len(categories) == 2


def test_delete_category_invalid_id(
    client, mock_user_data, mock_token_data, admins_data_inject, roles_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    delete_category = client.delete("/admin/category/2", headers=mock_token_data)

    assert delete_category.status_code == 500
    assert delete_category.json["success"] is False
    assert delete_category.json["location"] == "view soft delete category repo"


# ---------------------------------------------------------------------------- Admin logs Tests ----------------------------------------------------------------------------


def test_get_admin_logs(
    client,
    mock_category_data,
    mock_user_data,
    mock_token_data,
    admins_data_inject,
    db,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    create_category = client.post(
        "/admin/category", json=mock_category_data, headers=mock_token_data
    )

    assert create_category.status_code == 201

    get_admin_logs = client.get("/admin/logs", headers=mock_token_data)

    assert get_admin_logs.status_code == 200
    assert get_admin_logs.json["success"] is True
    assert get_admin_logs.json["message"] == "Admin logs fetched successfully"
    assert len(get_admin_logs.json["logs"]) == 1
    assert get_admin_logs.json["logs"][0]["action"] == "POST /admin/category"


# ---------------------------------------------------------------------------- Get all vendors test ----------------------------------------------------------------------------


def test_get_all_vendors(
    client,
    mock_user_data,
    mock_token_data,
    admins_data_inject,
    approved_vendor_profile_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    get_all_vendors = client.get(
        "/admin/vendors?page=1&per_page=1", headers=mock_token_data
    )

    assert get_all_vendors.status_code == 200
    assert get_all_vendors.json["success"] is True
    assert get_all_vendors.json["message"] == "Vendors fetched successfully"

    assert get_all_vendors.json["pagination"]["total"] == 1
    assert get_all_vendors.json["pagination"]["current_page"] == 1
    assert get_all_vendors.json["pagination"]["per_page"] == 1
    assert get_all_vendors.json["pagination"]["pages"] == 1

    assert len(get_all_vendors.json["vendors"]) == 3

    assert len(get_all_vendors.json["vendors"]["approved"]) == 1
    assert len(get_all_vendors.json["vendors"]["pending"]) == 0
    assert len(get_all_vendors.json["vendors"]["rejected"]) == 0


# ---------------------------------------------------------------------------- Vendor application approval Tests ----------------------------------------------------------------------------


def test_review_vendor_application(
    client,
    mock_user_data,
    mock_token_data,
    mock_admin_vendor_review_data,
    db,
    pending_vendor_profile_inject,
    admins_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    review_vendor_application = client.post(
        "/admin/vendor/1/review",
        json=mock_admin_vendor_review_data,
        headers=mock_token_data,
    )

    assert review_vendor_application.status_code == 200
    assert review_vendor_application.json["success"] is True


def test_review_vendor_application_action_validation_error(
    client,
    mock_user_data,
    mock_token_data,
    mock_admin_vendor_review_data,
    admins_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_admin_vendor_review_data["action"] = ""

    review_vendor_application = client.post(
        "/admin/vendor/1/review",
        json=mock_admin_vendor_review_data,
        headers=mock_token_data,
    )

    assert review_vendor_application.status_code == 400
    assert review_vendor_application.json["success"] is False
    assert (
        review_vendor_application.json["location"]
        == "view review vendor application request validation"
    )


def test_review_vendor_application_reason_validation_error(
    client,
    mock_user_data,
    mock_token_data,
    mock_admin_vendor_review_data,
    admins_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_admin_vendor_review_data["reason"] = "a" * 501

    review_vendor_application = client.post(
        "/admin/vendor/1/review",
        json=mock_admin_vendor_review_data,
        headers=mock_token_data,
    )

    assert review_vendor_application.status_code == 400
    assert review_vendor_application.json["success"] is False
    assert (
        review_vendor_application.json["location"]
        == "view review vendor application request validation"
    )


def test_review_vendor_application_repo_error(
    client,
    mock_user_data,
    mock_token_data,
    mock_admin_vendor_review_data,
    admins_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    review_vendor_application = client.post(
        "/admin/vendor/2/review",
        json=mock_admin_vendor_review_data,
        headers=mock_token_data,
    )

    assert review_vendor_application.status_code == 500
    assert review_vendor_application.json["success"] is False
    assert (
        review_vendor_application.json["location"]
        == "view review vendor application repo"
    )


# ---------------------------------------------------------------------------- Get all promotions ----------------------------------------------------------------------------


def test_get_all_promotions(
    client,
    mock_user_data,
    mock_token_data,
    admins_data_inject,
    promotions_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    get_all_promotions = client.get(
        "/admin/promotions?page=1&per_page=1", headers=mock_token_data
    )

    assert get_all_promotions.status_code == 200
    assert get_all_promotions.json["success"] is True
    assert get_all_promotions.json["message"] == "Promotions fetched successfully"

    assert get_all_promotions.json["pagination"]["total"] == 2
    assert get_all_promotions.json["pagination"]["current_page"] == 1
    assert get_all_promotions.json["pagination"]["per_page"] == 1
    assert get_all_promotions.json["pagination"]["pages"] == 2

    assert len(get_all_promotions.json["promotions"]) == 1
    assert len(get_all_promotions.json["promotions"][0]) == 10


# ---------------------------------------------------------------------------- Create promotion ----------------------------------------------------------------------------


def test_create_promotion(
    client,
    mock_user_data,
    mock_token_data,
    mock_promotion_data,
    admins_data_inject,
    products_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    create_promotion = client.post(
        "/admin/promotions", json=mock_promotion_data, headers=mock_token_data
    )

    assert create_promotion.status_code == 201
    assert create_promotion.json["success"] is True
    assert len(create_promotion.json["promotion"]) == 15


def test_create_promotion_title_validation_error(
    client,
    mock_user_data,
    mock_token_data,
    mock_promotion_data,
    admins_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_promotion_data["title"] = ""

    create_promotion = client.post(
        "/admin/promotions", json=mock_promotion_data, headers=mock_token_data
    )

    assert create_promotion.status_code == 400
    assert create_promotion.json["success"] is False
    assert (
        create_promotion.json["location"] == "view create promotion request validation"
    )


def test_create_promotion_code_validation_error(
    client,
    mock_user_data,
    mock_token_data,
    mock_promotion_data,
    admins_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_promotion_data["promo_code"] = "a"*21

    create_promotion = client.post(
        "/admin/promotions", json=mock_promotion_data, headers=mock_token_data
    )

    assert create_promotion.status_code == 400
    assert create_promotion.json["success"] is False
    assert (
        create_promotion.json["location"] == "view create promotion request validation"
    )


def test_create_promotion_discount_validation_error(
    client,
    mock_user_data,
    mock_token_data,
    mock_promotion_data,
    admins_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_promotion_data["discount_value"] = -1

    create_promotion = client.post(
        "/admin/promotions", json=mock_promotion_data, headers=mock_token_data
    )

    assert create_promotion.status_code == 400
    assert create_promotion.json["success"] is False
    assert (
        create_promotion.json["location"] == "view create promotion request validation"
    )


def test_create_promotion_promotion_type_validation_error(
    client,
    mock_user_data,
    mock_token_data,
    mock_promotion_data,
    admins_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_promotion_data["promotion_type"] = ""

    create_promotion = client.post(
        "/admin/promotions", json=mock_promotion_data, headers=mock_token_data
    )

    assert create_promotion.status_code == 400
    assert create_promotion.json["success"] is False
    assert (
        create_promotion.json["location"] == "view create promotion request validation"
    )


def test_create_promotion_image_url_validation_error(
    client,
    mock_user_data,
    mock_token_data,
    mock_promotion_data,
    admins_data_inject,
    products_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    # invalid url pattern
    mock_promotion_data["image_url"] = "t"

    create_promotion = client.post(
        "/admin/promotions", json=mock_promotion_data, headers=mock_token_data
    )

    assert create_promotion.status_code == 400
    assert create_promotion.json["success"] is False
    assert (
        create_promotion.json["location"] == "view create promotion request validation"
    )

    # test profile image too long
    mock_promotion_data["image_url"] = "https://example.com/profile.jpg" + "a" * 600

    create_promotion = client.post(
        "/admin/promotions", json=mock_promotion_data, headers=mock_token_data
    )

    assert create_promotion.status_code == 400
    assert create_promotion.json["success"] is False
    assert (
        create_promotion.json["location"] == "view create promotion request validation"
    )

    # post None
    mock_promotion_data["image_url"] = None

    create_promotion = client.post(
        "/admin/promotions", json=mock_promotion_data, headers=mock_token_data
    )

    assert create_promotion.status_code == 201


def test_create_promotion_repo_error(
    client,
    mock_user_data,
    mock_token_data,
    mock_promotion_data,
    admins_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    create_promotion = client.post(
        "/admin/promotions", json=mock_promotion_data, headers=mock_token_data
    )

    assert create_promotion.status_code == 500
    assert create_promotion.json["success"] is False
    assert create_promotion.json["location"] == "view create promotion repo"


# ---------------------------------------------------------------------------- test update promotion ----------------------------------------------------------------


def test_update_promotion(
    client,
    mock_user_data,
    mock_token_data,
    mock_promotion_data,
    admins_data_inject,
    roles_data_inject,
    promotions_data_inject,
    products_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    update_promotion = client.put(
        "/admin/promotions/1", json=mock_promotion_data, headers=mock_token_data
    )
    
    assert update_promotion.status_code == 200
    assert update_promotion.json["success"] is True
    assert update_promotion.json["message"] == "Promotion updated successfully"
    assert len(update_promotion.json["promotion"]) == 15


def test_update_promotion_title_validation_error(
    client,
    mock_user_data,
    mock_token_data,
    mock_promotion_data,
    admins_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_promotion_data["title"] = ""

    update_promotion = client.put(
        "/admin/promotions/1", json=mock_promotion_data, headers=mock_token_data
    )

    assert update_promotion.status_code == 400
    assert update_promotion.json["success"] is False
    assert (
        update_promotion.json["location"] ==  "view update promotion request validation"
    )


def test_update_promotion_code_validation_error(
    client,
    mock_user_data,
    mock_token_data,
    mock_promotion_data,
    admins_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_promotion_data["promo_code"] = "a" * 21

    update_promotion = client.put(
        "/admin/promotions/1", json=mock_promotion_data, headers=mock_token_data
    )

    assert update_promotion.status_code == 400
    assert update_promotion.json["success"] is False
    assert (
        update_promotion.json["location"] == "view update promotion request validation"
    )


def test_update_promotion_discount_validation_error(
    client,
    mock_user_data,
    mock_token_data,
    mock_promotion_data,
    admins_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_promotion_data["discount_value"] = -1

    update_promotion = client.put(
        "/admin/promotions/1", json=mock_promotion_data, headers=mock_token_data
    )

    assert update_promotion.status_code == 400
    assert update_promotion.json["success"] is False
    assert (
        update_promotion.json["location"] == "view update promotion request validation"
    )


def test_update_promotion_promotion_type_validation_error(
    client,
    mock_user_data,
    mock_token_data,
    mock_promotion_data,
    admins_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_promotion_data["promotion_type"] = ""

    update_promotion = client.put(
        "/admin/promotions/1", json=mock_promotion_data, headers=mock_token_data
    )

    assert update_promotion.status_code == 400
    assert update_promotion.json["success"] is False
    assert (
        update_promotion.json["location"] == "view update promotion request validation"
    )


def test_update_promotion_image_url_validation_error(
    client,
    mock_user_data,
    mock_token_data,
    mock_promotion_data,
    admins_data_inject,
    products_data_inject,
    promotions_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    # invalid url pattern
    mock_promotion_data["image_url"] = "t"

    update_promotion = client.put(
        "/admin/promotions/1", json=mock_promotion_data, headers=mock_token_data
    )

    assert update_promotion.status_code == 400
    assert update_promotion.json["success"] is False
    assert (
        update_promotion.json["location"] == "view update promotion request validation"
    )

    # test profile image too long
    mock_promotion_data["image_url"] = "https://example.com/profile.jpg" + "a" * 600

    update_promotion = client.put(
        "/admin/promotions/1", json=mock_promotion_data, headers=mock_token_data
    )

    assert update_promotion.status_code == 400
    assert update_promotion.json["success"] is False
    assert (
        update_promotion.json["location"] == "view update promotion request validation"
    )

    # post None
    mock_promotion_data["image_url"] = None

    update_promotion = client.put(
        "/admin/promotions/1", json=mock_promotion_data, headers=mock_token_data
    )

    assert update_promotion.status_code == 200


def test_update_promotion_repo_error(
    client,
    mock_user_data,
    mock_token_data,
    mock_promotion_data,
    admins_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    update_promotion = client.put(
        "/admin/promotions/1", json=mock_promotion_data, headers=mock_token_data
    )

    assert update_promotion.status_code == 500
    assert update_promotion.json["success"] is False
    assert update_promotion.json["location"] == "view update promotion repo"


# ------------------