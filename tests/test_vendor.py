# import models

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


def test_vendor_apply_duplicate(
    client, mock_user_data, mock_vendor_apply_data, mock_token_data, roles_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    apply_vendor = client.post(
        "/vendor/apply", json=mock_vendor_apply_data, headers=mock_token_data
    )

    assert apply_vendor.status_code == 201

    # apply again
    apply_vendor = client.post(
        "/vendor/apply", json=mock_vendor_apply_data, headers=mock_token_data
    )

    

    assert apply_vendor.status_code == 400
    assert apply_vendor.json["message"] == "Vendor already registered"
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
    client, mock_user_data, mock_vendor_apply_data, mock_token_data
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
    client, mock_user_data, mock_vendor_apply_data, mock_token_data
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
    client, mock_user_data, mock_vendor_apply_data, mock_token_data
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
    client, mock_user_data, mock_vendor_apply_data, mock_token_data
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
    client, mock_user_data, mock_vendor_apply_data, mock_token_data
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


# ----------------------------------------------------------------------------- Get vendor profile -----------------------------------------------------------

def test_get_vendor_profile(client, mock_user_data, mock_token_data, approved_vendor_profile_inject):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    get_vendor_profile = client.get("/vendor/profile", headers=mock_token_data)

    assert get_vendor_profile.status_code == 200
    assert get_vendor_profile.json["success"] is True
    assert len(get_vendor_profile.json["vendor"]) == 10


# ----------------------------------------------------------------------------- Get vendor products -----------------------------------------------------------

def test_get_vendor_products(client, mock_user_data, mock_token_data, approved_vendor_profile_inject, products_data_inject):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    get_vendor_products = client.get("/vendor/products?page=1&per_page=2", headers=mock_token_data)

    assert get_vendor_products.status_code == 200
    assert get_vendor_products.json["success"] is True
    assert len(get_vendor_products.json["products"]) == 1


# 
