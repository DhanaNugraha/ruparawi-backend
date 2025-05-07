from models.user import UserRole
# uv run pytest -v -s --cov=.
# uv run pytest tests/test_vendor.py -v -s --cov=. --cov-report term-missing


# ---------------------------------------------------------------------------- Vendor apply test ----------------------------------------------------------------------------


def test_vendor_apply(client, mock_user_data, mock_vendor_apply_data, mock_token_data, roles_data_inject):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    apply_vendor = client.post(
        "/vendor/apply", json=mock_vendor_apply_data, headers=mock_token_data
    )

    assert apply_vendor.status_code == 201
    assert (
        apply_vendor.json["message"]
        == f"Vendor {mock_vendor_apply_data['business_name']} application submitted for review"
    )
    assert apply_vendor.json["status"] == "pending"
    

def test_vendor_apply_name_validation_error(
    client, mock_user_data, mock_vendor_apply_data, mock_token_data, roles_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_vendor_apply_data["business_name"] = ""

    apply_vendor = client.post(
        "/vendor/apply", json=mock_vendor_apply_data, headers=mock_token_data
    )

    assert apply_vendor.status_code == 400
    assert apply_vendor.json["success"] is False
    assert apply_vendor.json["location"] == "view register vendor request validation"


def test_vendor_apply_email_validation_error(
    client, mock_user_data, mock_vendor_apply_data, mock_token_data, roles_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    # test empty email
    mock_vendor_apply_data["business_email"] = ""
    apply_vendor = client.post(
        "/vendor/apply", json=mock_vendor_apply_data, headers=mock_token_data
    )

    assert apply_vendor.status_code == 400
    assert apply_vendor.json["success"] is False
    assert apply_vendor.json["location"] == "view register vendor request validation"

    # test invalid email pattern
    mock_vendor_apply_data["business_email"] = "invalid_email_pattern"
    apply_vendor = client.post(
        "/vendor/apply", json=mock_vendor_apply_data, headers=mock_token_data
    )

    assert apply_vendor.status_code == 400
    assert apply_vendor.json["success"] is False
    assert apply_vendor.json["location"] == "view register vendor request validation"

    # test consecutive dots in email
    mock_vendor_apply_data["business_email"] = "a@bc..com"
    apply_vendor = client.post(
        "/vendor/apply", json=mock_vendor_apply_data, headers=mock_token_data
    )

    assert apply_vendor.status_code == 400
    assert apply_vendor.json["success"] is False
    assert apply_vendor.json["location"] == "view register vendor request validation"

    # test email too long
    mock_vendor_apply_data["business_email"] = "a" * 256 + "@example.com"
    apply_vendor = client.post(
        "/vendor/apply", json=mock_vendor_apply_data, headers=mock_token_data
    )

    assert apply_vendor.status_code == 400
    assert apply_vendor.json["success"] is False
    assert apply_vendor.json["location"] == "view register vendor request validation"


def test_vendor_apply_phone_validation_error(
    client, mock_user_data, mock_vendor_apply_data, mock_token_data, roles_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    # test empty phone
    mock_vendor_apply_data["business_phone"] = ""
    apply_vendor = client.post(
        "/vendor/apply", json=mock_vendor_apply_data, headers=mock_token_data
    )

    assert apply_vendor.status_code == 400
    assert apply_vendor.json["success"] is False
    assert apply_vendor.json["location"] == "view register vendor request validation"

    # test invalid phone pattern
    mock_vendor_apply_data["business_phone"] = "invalid_email_pattern"
    apply_vendor = client.post(
        "/vendor/apply", json=mock_vendor_apply_data, headers=mock_token_data
    )

    assert apply_vendor.status_code == 400
    assert apply_vendor.json["success"] is False
    assert apply_vendor.json["location"] == "view register vendor request validation"


def test_vendor_apply_address_validation_error(
    client, mock_user_data, mock_vendor_apply_data, mock_token_data, roles_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    # test empty address
    mock_vendor_apply_data["business_address"] = ""
    apply_vendor = client.post(
        "/vendor/apply", json=mock_vendor_apply_data, headers=mock_token_data
    )

    assert apply_vendor.status_code == 400
    assert apply_vendor.json["success"] is False
    assert apply_vendor.json["location"] == "view register vendor request validation"


def test_vendor_apply_description_validation_error(
    client, mock_user_data, mock_vendor_apply_data, mock_token_data, roles_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    # test description too long
    mock_vendor_apply_data["business_description"] = "a" * 501
    apply_vendor = client.post(
        "/vendor/apply", json=mock_vendor_apply_data, headers=mock_token_data
    )

    assert apply_vendor.status_code == 400
    assert apply_vendor.json["success"] is False
    assert apply_vendor.json["location"] == "view register vendor request validation"


def test_vendor_apply_logo_validation_error(
    client, mock_user_data, mock_vendor_apply_data, mock_token_data, roles_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    # test logo url invalid pattern
    mock_vendor_apply_data["business_logo_url"] = "a" 
    apply_vendor = client.post(
        "/vendor/apply", json=mock_vendor_apply_data, headers=mock_token_data
    )

    assert apply_vendor.status_code == 400
    assert apply_vendor.json["success"] is False
    assert apply_vendor.json["location"] == "view register vendor request validation"

    # test logo url too long
    mock_vendor_apply_data["business_logo_url"] = (
        "https://example.com/profile.jpg" + "a" * 600
    )
    apply_vendor = client.post(
        "/vendor/apply", json=mock_vendor_apply_data, headers=mock_token_data
    )

    assert apply_vendor.status_code == 400
    assert apply_vendor.json["success"] is False
    assert apply_vendor.json["location"] == "view register vendor request validation"

    # test empty logo url
    mock_vendor_apply_data["business_logo_url"] = ""
    apply_vendor = client.post(
        "/vendor/apply", json=mock_vendor_apply_data, headers=mock_token_data
    )

    assert apply_vendor.status_code == 201


def test_vendor_apply_repo_error(
    client, mock_user_data, mock_vendor_apply_data, mock_token_data, roles_data_inject, db
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    # delete vendor role
    role = db.session.execute(
        db.select(UserRole)
        .filter(UserRole.name == "vendor")
    ).scalar_one_or_none()

    db.session.delete(role)

    # run 
    apply_vendor = client.post(
        "/vendor/apply", json=mock_vendor_apply_data, headers=mock_token_data
    )

    assert apply_vendor.status_code == 500
    assert apply_vendor.json["success"] is False
    assert apply_vendor.json["location"] == "view register vendor repo"


# ----------------------------------------------------------------------------- Get vendor profile -----------------------------------------------------------


def test_get_vendor_profile(
    client,
    mock_user_data,
    mock_token_data,
    approved_vendor_profile_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    get_vendor_profile = client.get("/vendor/profile", headers=mock_token_data)

    assert get_vendor_profile.status_code == 200
    assert get_vendor_profile.json["success"] is True
    assert len(get_vendor_profile.json["vendor"]) == 10


# ----------------------------------------------------------------------------- Get update vendor profile-----------------------------------------------------------


def test_update_vendor_profile(
    client,
    mock_user_data,
    mock_token_data,
    approved_vendor_profile_inject,
    roles_data_inject,
    mock_vendor_update_data,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    update_vendor_profile = client.put(
        "/vendor/profile", json=mock_vendor_update_data, headers=mock_token_data
    )

    assert update_vendor_profile.status_code == 200
    assert update_vendor_profile.json["success"] is True


def test_vendor_update_name_validation_error(
    client, mock_user_data, mock_vendor_update_data, mock_token_data, roles_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_vendor_update_data["business_name"] = ""

    update_vendor_profile = client.put(
        "/vendor/profile", json=mock_vendor_update_data, headers=mock_token_data
    )

    assert update_vendor_profile.status_code == 400
    assert update_vendor_profile.json["success"] is False
    assert (
        update_vendor_profile.json["location"]
        == "view update vendor profile request validation"
    )


def test_vendor_update_email_validation_error(
    client, mock_user_data, mock_vendor_update_data, mock_token_data, roles_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    # test empty email
    mock_vendor_update_data["business_email"] = ""
    update_vendor_profile = client.put(
        "/vendor/profile", json=mock_vendor_update_data, headers=mock_token_data
    )

    assert update_vendor_profile.status_code == 400
    assert update_vendor_profile.json["success"] is False
    assert (
        update_vendor_profile.json["location"]
        == "view update vendor profile request validation"
    )

    # test invalid email pattern
    mock_vendor_update_data["business_email"] = "invalid_email_pattern"
    update_vendor_profile = client.put(
        "/vendor/profile", json=mock_vendor_update_data, headers=mock_token_data
    )

    assert update_vendor_profile.status_code == 400
    assert update_vendor_profile.json["success"] is False
    assert (
        update_vendor_profile.json["location"]
        == "view update vendor profile request validation"
    )

    # test consecutive dots in email
    mock_vendor_update_data["business_email"] = "a@bc..com"
    update_vendor_profile = client.put(
        "/vendor/profile", json=mock_vendor_update_data, headers=mock_token_data
    )

    assert update_vendor_profile.status_code == 400
    assert update_vendor_profile.json["success"] is False
    assert (
        update_vendor_profile.json["location"]
        == "view update vendor profile request validation"
    )

    # test email too long
    mock_vendor_update_data["business_email"] = "a" * 256 + "@example.com"
    update_vendor_profile = client.put(
        "/vendor/profile", json=mock_vendor_update_data, headers=mock_token_data
    )

    assert update_vendor_profile.status_code == 400
    assert update_vendor_profile.json["success"] is False
    assert (
        update_vendor_profile.json["location"]
        == "view update vendor profile request validation"
    )


def test_vendor_update_phone_validation_error(
    client, mock_user_data, mock_vendor_update_data, mock_token_data, roles_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    # test empty phone
    mock_vendor_update_data["business_phone"] = ""
    update_vendor_profile = client.put(
        "/vendor/profile", json=mock_vendor_update_data, headers=mock_token_data
    )

    assert update_vendor_profile.status_code == 400
    assert update_vendor_profile.json["success"] is False
    assert (
        update_vendor_profile.json["location"]
        == "view update vendor profile request validation"
    )

    # test invalid phone pattern
    mock_vendor_update_data["business_phone"] = "invalid_email_pattern"
    update_vendor_profile = client.put(
        "/vendor/profile", json=mock_vendor_update_data, headers=mock_token_data
    )

    assert update_vendor_profile.status_code == 400
    assert update_vendor_profile.json["success"] is False
    assert (
        update_vendor_profile.json["location"]
        == "view update vendor profile request validation"
    )


def test_vendor_update_address_validation_error(
    client, mock_user_data, mock_vendor_update_data, mock_token_data, roles_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    # test empty address
    mock_vendor_update_data["business_address"] = ""
    update_vendor_profile = client.put(
        "/vendor/profile", json=mock_vendor_update_data, headers=mock_token_data
    )

    assert update_vendor_profile.status_code == 400
    assert update_vendor_profile.json["success"] is False
    assert (
        update_vendor_profile.json["location"]
        == "view update vendor profile request validation"
    )


def test_vendor_update_description_validation_error(
    client, mock_user_data, mock_vendor_update_data, mock_token_data, roles_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    # test description too long
    mock_vendor_update_data["business_description"] = "a" * 501
    update_vendor_profile = client.put(
        "/vendor/profile", json=mock_vendor_update_data, headers=mock_token_data
    )

    assert update_vendor_profile.status_code == 400
    assert update_vendor_profile.json["success"] is False
    assert (
        update_vendor_profile.json["location"]
        == "view update vendor profile request validation"
    )


def test_vendor_update_logo_validation_error(
    client,
    mock_user_data,
    mock_vendor_update_data,
    mock_token_data,
    roles_data_inject,
    approved_vendor_profile_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    # test logo url invalid pattern
    mock_vendor_update_data["business_logo_url"] = "a"
    update_vendor_profile = client.put(
        "/vendor/profile", json=mock_vendor_update_data, headers=mock_token_data
    )

    assert update_vendor_profile.status_code == 400
    assert update_vendor_profile.json["success"] is False
    assert (
        update_vendor_profile.json["location"]
        == "view update vendor profile request validation"
    )

    # test logo url too long
    mock_vendor_update_data["business_logo_url"] = (
        "https://example.com/profile.jpg" + "a" * 600
    )
    update_vendor_profile = client.put(
        "/vendor/profile", json=mock_vendor_update_data, headers=mock_token_data
    )

    assert update_vendor_profile.status_code == 400
    assert update_vendor_profile.json["success"] is False
    assert (
        update_vendor_profile.json["location"]
        == "view update vendor profile request validation"
    )

    # test empty logo url
    mock_vendor_update_data["business_logo_url"] = ""
    update_vendor_profile = client.put(
        "/vendor/profile", json=mock_vendor_update_data, headers=mock_token_data
    )

    assert update_vendor_profile.status_code == 200


# ----------------------------------------------------------------------------- Get vendor products -----------------------------------------------------------


def test_get_vendor_products(
    client,
    mock_user_data,
    mock_token_data,
    approved_vendor_profile_inject,
    products_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    get_vendor_products = client.get("/vendor/products?page=1&per_page=2", headers=mock_token_data)

    assert get_vendor_products.status_code == 200
    assert get_vendor_products.json["success"] is True
    assert len(get_vendor_products.json["products"]) == 2


# ----------------------------------------------------------------------------- Get vendor stats -----------------------------------------------------------

def test_get_vendor_stats(
    client,
    mock_user_data,
    mock_token_data,
    approved_vendor_profile_inject,
    order_data_inject,
    order_item_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    get_vendor_stats = client.get("/vendor/stats", headers=mock_token_data)

    vendor_stats = get_vendor_stats.json["vendor_stats"]

    assert get_vendor_stats.status_code == 200
    assert get_vendor_stats.json["success"] is True
    assert vendor_stats["total_orders"] == 2
    assert vendor_stats["total_customers"] == 1
    assert vendor_stats["total_revenue"] == 30.0
    assert vendor_stats["total_sales"] == 3
    assert len(vendor_stats["monthly_revenue"]) == 1
    assert len(vendor_stats["monthly_orders"]) == 1


# ----------------------------------------------------------------------------- Get vendor recent orders -----------------------------------------------------------


def test_get_vendor_recent_orders(
    client,
    mock_user_data,
    mock_token_data,
    products_data_inject,
    approved_vendor_profile_inject,
    order_data_inject,
    order_item_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    get_vendor_recent_orders = client.get("/vendor/recent-orders", headers=mock_token_data)

    recent_orders = get_vendor_recent_orders.json["recent_orders"]

    assert get_vendor_recent_orders.status_code == 200
    assert get_vendor_recent_orders.json["success"] is True
    assert len(recent_orders) == 2
    assert len(recent_orders[0]) == 9


# repo 41-53 in admin
# repo 57-65 in admin

# views\vendor.py               53     11    79%   65-66, 105-107, 141-142, 165-166, 202-203