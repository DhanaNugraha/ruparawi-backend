import models

# uv run pytest -v -s --cov=.
# uv run pytest tests/test_admin.py -v -s --cov=.


# ---------------------------------------------------------------------------- Admin route Test ----------------------------------------------------------------------------

def test_admin_required(client, mock_user_data, mock_token_data):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    admin_route = client.post("/admin/category", headers=mock_token_data)

    assert admin_route.status_code == 403


# ---------------------------------------------------------------------------- Create category Tests ----------------------------------------------------------------------------

def test_create_category(client, mock_user_data, mock_token_data, mock_category_data, db, admins_data_inject):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    create_category = client.post("/admin/category", json=mock_category_data, headers=mock_token_data)

    assert create_category.status_code == 201
    assert create_category.json["success"] is True
    assert create_category.json["message"] == "Category created successfully"
    assert create_category.json["category"]["name"] == mock_category_data["name"]

    categories = db.session.execute(db.select(models.ProductCategory)).scalars().all()

    assert len(categories) == 1
    assert categories[0].name == mock_category_data["name"]


def test_create_category_name_validation_error(client, mock_user_data, mock_token_data, mock_category_data, admins_data_inject):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_category_data["name"] = ""
    create_category = client.post("/admin/category", json=mock_category_data, headers=mock_token_data)

    assert create_category.status_code == 400
    assert create_category.json["success"] is False
    assert create_category.json["location"] == "view create category request validation"


def test_create_subcategory(client, mock_user_data, mock_token_data, mock_subcategory_data, db, admins_data_inject, category_data_inject):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    create_subcategory = client.post("/admin/category", json=mock_subcategory_data, headers=mock_token_data)

    assert create_subcategory.status_code == 201
    assert create_subcategory.json["success"] is True
    assert create_subcategory.json["message"] == "Category created successfully"

    categories = db.session.execute(db.select(models.ProductCategory).filter_by(parent_category_id=2)).scalar_one_or_none()

    assert categories.name == mock_subcategory_data["name"]


def test_create_subcategory_parent_category_invalid(client, mock_user_data, mock_token_data, mock_subcategory_data, admins_data_inject):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    create_subcategory = client.post(
        "/admin/category", json=mock_subcategory_data, headers=mock_token_data
    )

    assert create_subcategory.status_code == 500
    assert create_subcategory.json["success"] is False
    assert create_subcategory.json["location"] == "view create category repo"


# ---------------------------------------------------------------------------- Update category Tests ----------------------------------------------------------------------------

def test_update_category(client, mock_user_data, mock_token_data, mock_update_category_data, db, category_data_inject, admins_data_inject):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    update_category = client.put(
        "/admin/category/1", json=mock_update_category_data, headers=mock_token_data
    )

    assert update_category.status_code == 200
    assert update_category.json["success"] is True
    assert update_category.json["message"] == "Category updated successfully"
    assert update_category.json["category"]["name"] == mock_update_category_data["name"]

    categories = db.session.execute(db.select(models.ProductCategory).filter_by(id = 1)).scalar_one_or_none()

    assert categories.name == mock_update_category_data["name"]


def test_update_category_validation_error(client, mock_user_data, mock_token_data, mock_update_category_data, admins_data_inject):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_update_category_data["name"] = ""

    update_category = client.put(
        "/admin/category/1", json=mock_update_category_data, headers=mock_token_data
    )

    assert update_category.status_code == 400
    assert update_category.json["success"] is False
    assert update_category.json["location"] == "view update category request validation"


def test_update_category_parent_category_invalid(client, mock_user_data, mock_token_data, mock_update_category_data, db, category_data_inject, admins_data_inject):
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


def test_delete_category(client, mock_user_data, mock_token_data, db, category_data_inject, admins_data_inject):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    delete_category = client.delete("/admin/category/1", headers=mock_token_data)

    assert delete_category.status_code == 200
    assert delete_category.json["success"] is True
    assert (
        delete_category.json["message"]
        == "Category tree soft deleted (archived) successfully"
    )

    categories = db.session.execute(db.select(models.ProductCategory).filter_by(id = 1)).scalar_one_or_none()

    assert categories.is_active is False


def test_delete_category_tree(client, mock_category_data,  mock_subcategory_data, mock_user_data, mock_token_data, admins_data_inject, db):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    create_category = client.post("/admin/category", json=mock_category_data, headers=mock_token_data)

    assert create_category.status_code == 201

    mock_subcategory_data["parent_category_id"] = 1

    create_subcategory = client.post("/admin/category", json=mock_subcategory_data, headers=mock_token_data)

    assert create_subcategory.status_code == 201

    delete_category = client.delete("/admin/category/1", headers=mock_token_data)

    assert delete_category.status_code == 200

    categories = db.session.execute(db.select(models.ProductCategory).filter_by(is_active = False)).scalars().all()

    assert len(categories) == 2


def test_delete_category_invalid_id(client, mock_user_data, mock_token_data, admins_data_inject):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    delete_category = client.delete("/admin/category/2", headers=mock_token_data)

    assert delete_category.status_code == 500
    assert delete_category.json["success"] is False
    assert delete_category.json["location"] == "view soft delete category repo"


# ---------------------------------------------------------------------------- Admin logs Tests ----------------------------------------------------------------------------


def test_admin_logs(client, mock_category_data, mock_user_data, mock_token_data, admins_data_inject, db):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    create_category = client.post("/admin/category", json=mock_category_data, headers=mock_token_data)

    assert create_category.status_code == 201

    admin_log = db.session.execute(db.select(models.AdminLog).filter_by(id = 1)).scalar_one_or_none()

    assert admin_log.action == "POST /admin/category"
    assert admin_log.admin_id == 1


# test for vendor approval
