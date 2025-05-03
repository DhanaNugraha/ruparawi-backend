import models

# uv run pytest -v -s --cov=.
# uv run pytest tests/test_user.py -v -s --cov=.
# uv run pytest tests/test_user.py -v -s --cov=. --cov-report term-missing


# ---------------------------------------------------------------------------- Get public profile ----------------------------------------------------------------------------


def test_get_public_profile(client, users_data_inject):
    public_user = client.get("/user/1")

    assert public_user.status_code == 200
    assert public_user.json["success"] is True
    assert public_user.json["user"]["id"] == 1
    assert public_user.json["user"]["username"] == "john"
    assert len(public_user.json["user"]) == 8


def test_get_public_profile_not_exist(client, users_data_inject):
    public_user = client.get("/user/100")

    assert public_user.status_code == 500
    assert public_user.json["success"] is False


# ---------------------------------------------------------------------------- Update user ----------------------------------------------------------------------------


def test_update_user(
    client, mock_user_data, mock_token_data, mock_update_user_data, db, roles_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    update_user = client.put(
        "/user/me", json=mock_update_user_data, headers=mock_token_data
    )

    assert update_user.status_code == 200
    assert update_user.json["success"] is True
    assert update_user.json["message"] == "Profile updated successfully"

    user = db.session.execute(
        db.select(models.User).filter_by(email=mock_user_data["email"])
    ).scalar_one()

    assert user.id == 1
    assert user.username == mock_user_data["username"]
    assert user.bio == mock_update_user_data["bio"]
    assert user.first_name == mock_update_user_data["first_name"]
    assert user.last_name == mock_update_user_data["last_name"]


def test_update_user_bio_error(
    client, mock_user_data, mock_token_data, mock_update_user_data, roles_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_update_user_data["bio"] = "a" * 600

    update_user = client.put(
        "/user/me", json=mock_update_user_data, headers=mock_token_data
    )

    assert update_user.status_code == 400
    assert update_user.json["success"] is False
    assert update_user.json["location"] == "view update user profile request validation"


def test_update_user_profile_image_error(
    client, mock_user_data, mock_token_data, mock_update_user_data, roles_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    # invalid url pattern
    mock_update_user_data["profile_image_url"] = "t"

    update_user = client.put(
        "/user/me", json=mock_update_user_data, headers=mock_token_data
    )

    assert update_user.status_code == 400
    assert update_user.json["success"] is False
    assert update_user.json["location"] == "view update user profile request validation"

    # test profile image too long
    mock_update_user_data["profile_image_url"] = (
        "https://example.com/profile.jpg" + "a" * 600
    )

    update_user = client.put(
        "/user/me", json=mock_update_user_data, headers=mock_token_data
    )

    assert update_user.status_code == 400
    assert update_user.json["success"] is False
    assert update_user.json["location"] == "view update user profile request validation"

    # post None
    mock_update_user_data["profile_image_url"] = None

    update_user = client.put(
        "/user/me", json=mock_update_user_data, headers=mock_token_data
    )

    assert update_user.status_code == 200


def test_update_user_password_validation_error(
    client, mock_user_data, mock_token_data, mock_update_user_data, roles_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_update_user_data["password"] = "" 

    update_user = client.put(
        "/user/me", json=mock_update_user_data, headers=mock_token_data
    )

    assert update_user.status_code == 400
    assert update_user.json["success"] is False
    assert update_user.json["location"] == "view update user profile request validation"


# ---------------------------------------------------------------------------- Create user address ----------------------------------------------------------------------------

def test_create_user_address(client, mock_user_data, mock_token_data, mock_create_address_data, roles_data_inject):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    create_user_address = client.post(
        "/user/me/address", json=mock_create_address_data, headers=mock_token_data
    )

    assert create_user_address.status_code == 201
    assert create_user_address.json["success"] is True  
    assert create_user_address.json["message"] == "Address added successfully"


def test_create_address_address1_validation_error(client, mock_user_data, mock_token_data, mock_create_address_data, roles_data_inject):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_create_address_data["address_line1"] = "" 

    create_user_address = client.post(
        "/user/me/address", json=mock_create_address_data, headers=mock_token_data
    )

    assert create_user_address.status_code == 400
    assert create_user_address.json["success"] is False
    assert create_user_address.json["location"] == "view add address request validation"


def test_create_address_address2_validation_error(
    client, mock_user_data, mock_token_data, mock_create_address_data, roles_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_create_address_data["address_line2"] = "a" * 101

    create_user_address = client.post(
        "/user/me/address", json=mock_create_address_data, headers=mock_token_data
    )

    assert create_user_address.status_code == 400
    assert create_user_address.json["success"] is False
    assert create_user_address.json["location"] == "view add address request validation"


def test_create_address_city_validation_error(
    client, mock_user_data, mock_token_data, mock_create_address_data, roles_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_create_address_data["city"] = ""

    create_user_address = client.post(
        "/user/me/address", json=mock_create_address_data, headers=mock_token_data
    )

    assert create_user_address.status_code == 400
    assert create_user_address.json["success"] is False
    assert create_user_address.json["location"] == "view add address request validation"


def test_create_address_state_validation_error(
    client, mock_user_data, mock_token_data, mock_create_address_data, roles_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_create_address_data["state"] = ""

    create_user_address = client.post(
        "/user/me/address", json=mock_create_address_data, headers=mock_token_data
    )

    assert create_user_address.status_code == 400
    assert create_user_address.json["success"] is False
    assert create_user_address.json["location"] == "view add address request validation"


def test_create_address_postal_code_validation_error(
    client, mock_user_data, mock_token_data, mock_create_address_data, roles_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_create_address_data["postal_code"] = ""

    create_user_address = client.post(
        "/user/me/address", json=mock_create_address_data, headers=mock_token_data
    )

    assert create_user_address.status_code == 400
    assert create_user_address.json["success"] is False
    assert create_user_address.json["location"] == "view add address request validation"


def test_create_address_country_validation_error(
    client, mock_user_data, mock_token_data, mock_create_address_data, roles_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_create_address_data["country"] = ""

    create_user_address = client.post(
        "/user/me/address", json=mock_create_address_data, headers=mock_token_data
    )

    assert create_user_address.status_code == 400
    assert create_user_address.json["success"] is False
    assert create_user_address.json["location"] == "view add address request validation"


# ---------------------------------------------------------------------------- Get user address ----------------------------------------------------------------------------


def test_get_user_address(client, mock_user_data, mock_token_data, address_data_inject, roles_data_inject):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    create_user_address = client.get(
        "/user/me/address", headers=mock_token_data
    )

    assert create_user_address.status_code == 200
    assert create_user_address.json["success"] is True  
    assert len(create_user_address.json["addresses"]) == 1
    assert len(create_user_address.json["addresses"][0]) == 9


# ---------------------------------------------------------------------------- Update user address ----------------------------------------------------------------------------


def test_update_address(
    client,
    mock_user_data,
    mock_token_data,
    mock_update_address_data,
    address_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    updated_address = client.put(
        "/user/me/address/1", json=mock_update_address_data, headers=mock_token_data
    )

    assert updated_address.status_code == 200
    assert updated_address.json["success"] is True
    assert updated_address.json["message"] == "Address updated successfully"



def test_update_address_address1_validation_error(
    client, mock_user_data, mock_token_data, mock_update_address_data, roles_data_inject, address_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_update_address_data["address_line1"] = ""

    updated_address = client.put(
        "/user/me/address/1", json=mock_update_address_data, headers=mock_token_data
    )

    assert updated_address.status_code == 400
    assert updated_address.json["success"] is False
    assert updated_address.json["location"] == "view update address request validation"


def test_update_address_address2_validation_error(
    client, mock_user_data, mock_token_data, mock_update_address_data, roles_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_update_address_data["address_line2"] = "a" * 101

    updated_address = client.put(
        "/user/me/address/1", json=mock_update_address_data, headers=mock_token_data
    )

    assert updated_address.status_code == 400
    assert updated_address.json["success"] is False
    assert updated_address.json["location"] == "view update address request validation"


def test_update_address_city_validation_error(
    client, mock_user_data, mock_token_data, mock_update_address_data, roles_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_update_address_data["city"] = ""

    updated_address = client.put(
        "/user/me/address/1", json=mock_update_address_data, headers=mock_token_data
    )

    assert updated_address.status_code == 400
    assert updated_address.json["success"] is False
    assert updated_address.json["location"] == "view update address request validation"


def test_update_address_state_validation_error(
    client, mock_user_data, mock_token_data, mock_update_address_data, roles_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_update_address_data["state"] = ""

    updated_address = client.put(
        "/user/me/address/1", json=mock_update_address_data, headers=mock_token_data
    )

    assert updated_address.status_code == 400
    assert updated_address.json["success"] is False
    assert updated_address.json["location"] == "view update address request validation"


def test_update_address_postal_code_validation_error(
    client, mock_user_data, mock_token_data, mock_update_address_data, roles_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_update_address_data["postal_code"] = ""

    updated_address = client.put(
        "/user/me/address/1", json=mock_update_address_data, headers=mock_token_data
    )

    assert updated_address.status_code == 400
    assert updated_address.json["success"] is False
    assert updated_address.json["location"] == "view update address request validation"


def test_update_address_country_validation_error(
    client, mock_user_data, mock_token_data, mock_update_address_data, roles_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_update_address_data["country"] = ""

    updated_address = client.put(
        "/user/me/address/1", json=mock_update_address_data, headers=mock_token_data
    )

    assert updated_address.status_code == 400
    assert updated_address.json["success"] is False
    assert updated_address.json["location"] == "view update address request validation"


def test_update_address_repo_error(
    client, mock_user_data, mock_token_data, mock_update_address_data, roles_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    updated_address = client.put(
        "/user/me/address/1", json=mock_update_address_data, headers=mock_token_data
    )

    assert updated_address.status_code == 500
    assert updated_address.json["success"] is False
    assert updated_address.json["location"] == "view update address repo"


# ---------------------------------------------------------------------------- Delete user address ----------------------------------------------------------------------------


def test_delete_address(client, mock_user_data, mock_token_data, roles_data_inject, address_data_inject):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    delete_address = client.delete("/user/me/address/1", headers=mock_token_data)

    assert delete_address.status_code == 200
    assert delete_address.json["success"] is True
    assert delete_address.json["message"] == "Address deleted successfully"


def test_delete_address_repo_error(
    client, mock_user_data, mock_token_data, roles_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    delete_address = client.delete("/user/me/address/1", headers=mock_token_data)

    assert delete_address.status_code == 500
    assert delete_address.json["success"] is False
    assert delete_address.json["location"] == "view delete address repo"


# ---------------------------------------------------------------------------- Create user payment ----------------------------------------------------------------------------


def test_create_payment_method(client, mock_user_data, mock_token_data, mock_create_payment_method_data, roles_data_inject):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    create_payment_method = client.post(
        "/user/me/payment-methods", json=mock_create_payment_method_data, headers=mock_token_data
    )

    assert create_payment_method.status_code == 201
    assert create_payment_method.json["success"] is True
    assert len(create_payment_method.json["message"]) == 7


def test_create_payment_method_payment_type_validation_error(
    client,
    mock_user_data,
    mock_token_data,
    mock_create_payment_method_data,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_create_payment_method_data["payment_type"] = "a"

    create_payment_method = client.post(
        "/user/me/payment-methods",
        json=mock_create_payment_method_data,
        headers=mock_token_data,
    )

    assert create_payment_method.status_code == 400
    assert create_payment_method.json["success"] is False
    assert (
        create_payment_method.json["location"]
        == "view add payment method request validation"
    )


def test_create_payment_method_provider_validation_error(
    client,
    mock_user_data,
    mock_token_data,
    mock_create_payment_method_data,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_create_payment_method_data["provider"] = ""

    create_payment_method = client.post(
        "/user/me/payment-methods",
        json=mock_create_payment_method_data,
        headers=mock_token_data,
    )

    assert create_payment_method.status_code == 400
    assert create_payment_method.json["success"] is False
    assert (
        create_payment_method.json["location"]
        == "view add payment method request validation"
    )


def test_create_payment_method_account_number_validation_error(    
    client, mock_user_data, mock_token_data, mock_create_payment_method_data, roles_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_create_payment_method_data["account_number"] = ""

    create_payment_method = client.post(
        "/user/me/payment-methods", json=mock_create_payment_method_data, headers=mock_token_data
    )

    assert create_payment_method.status_code == 400
    assert create_payment_method.json["success"] is False
    assert (
        create_payment_method.json["location"]
        == "view add payment method request validation"
    )


def test_create_payment_method_expiry_date_validation_error(
    client,
    mock_user_data,
    mock_token_data,
    mock_create_payment_method_data,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_create_payment_method_data["expiry_date"] = ""

    create_payment_method = client.post(
        "/user/me/payment-methods",
        json=mock_create_payment_method_data,
        headers=mock_token_data,
    )

    assert create_payment_method.status_code == 400
    assert create_payment_method.json["success"] is False
    assert (
        create_payment_method.json["location"]
        == "view add payment method request validation"
    )


# ---------------------------------------------------------------------------- Get all user payment ----------------------------------------------------------------------------

def test_get_payment_method(client, mock_user_data, mock_token_data, payment_method_data_inject, roles_data_inject):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    get_payment_method = client.get("/user/me/payment-methods", headers=mock_token_data)

    assert get_payment_method.status_code == 200
    assert get_payment_method.json["success"] is True
    assert len(get_payment_method.json["payment_methods"]) == 1
    assert len(get_payment_method.json["payment_methods"][0]) == 7


# ----------------------------------------------------------------------------- Update user payment ----------------------------------------------------------------------------


def test_update_payment_method(client, mock_user_data, mock_token_data, mock_update_payment_method_data, payment_method_data_inject, roles_data_inject):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    update_payment_method = client.put(
        "/user/me/payment-methods/1", json=mock_update_payment_method_data, headers=mock_token_data
    )

    assert update_payment_method.status_code == 200
    assert update_payment_method.json["success"] is True
    assert len(update_payment_method.json["message"]) == 7


def test_update_payment_method_payment_type_validation_error(
    client,
    mock_user_data,
    mock_token_data,
    mock_update_payment_method_data,
    payment_method_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_update_payment_method_data["payment_type"] = "a"

    update_payment_method = client.put(
        "/user/me/payment-methods/1",
        json=mock_update_payment_method_data,
        headers=mock_token_data,
    )

    assert update_payment_method.status_code == 400
    assert update_payment_method.json["success"] is False
    assert (
        update_payment_method.json["location"]
        == "view update payment method request validation"
    )


def test_update_payment_method_provider_validation_error(
    client,
    mock_user_data,
    mock_token_data,
    mock_update_payment_method_data,
    payment_method_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_update_payment_method_data["provider"] = ""

    update_payment_method = client.put(
        "/user/me/payment-methods/1",
        json=mock_update_payment_method_data,
        headers=mock_token_data,
    )

    assert update_payment_method.status_code == 400
    assert update_payment_method.json["success"] is False
    assert (
        update_payment_method.json["location"]
        == "view update payment method request validation"
    )


def test_update_payment_method_account_number_validation_error(
    client,
    mock_user_data,
    mock_token_data,
    mock_update_payment_method_data,
    payment_method_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_update_payment_method_data["account_number"] = ""

    update_payment_method = client.put(
        "/user/me/payment-methods/1",
        json=mock_update_payment_method_data,
        headers=mock_token_data,
    )

    assert update_payment_method.status_code == 400
    assert update_payment_method.json["success"] is False
    assert (
        update_payment_method.json["location"]
        == "view update payment method request validation"
    )


def test_update_payment_method_expiry_date_validation_error(
    client,
    mock_user_data,
    mock_token_data,
    mock_update_payment_method_data,
    payment_method_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_update_payment_method_data["expiry_date"] = "2000-12-31"

    update_payment_method = client.put(
        "/user/me/payment-methods/1",
        json=mock_update_payment_method_data,
        headers=mock_token_data,
    )

    assert update_payment_method.status_code == 400
    assert update_payment_method.json["success"] is False
    assert (
        update_payment_method.json["location"]
        == "view update payment method request validation"
    )


def test_update_payment_method_repo_error(
    client,
    mock_user_data,
    mock_token_data,
    mock_update_payment_method_data,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    update_payment_method = client.put(
        "/user/me/payment-methods/1",
        json=mock_update_payment_method_data,
        headers=mock_token_data,
    )

    assert update_payment_method.status_code == 500
    assert update_payment_method.json["success"] is False
    assert update_payment_method.json["location"] == "view update payment method repo"


# ----------------------------------------------------------------------------- Delete user payment ----------------------------------------------------------------------------

def test_delete_payment_method(client, mock_user_data, mock_token_data, payment_method_data_inject, roles_data_inject):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    delete_payment_method = client.delete("/user/me/payment-methods/1", headers=mock_token_data)

    assert delete_payment_method.status_code == 200
    assert delete_payment_method.json["success"] is True
    assert delete_payment_method.json["message"] == "Payment method deleted successfully"


def test_delete_payment_method_repo_error(
    client,
    mock_user_data,
    mock_token_data,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    delete_payment_method = client.delete(
        "/user/me/payment-methods/1", headers=mock_token_data
    )

    assert delete_payment_method.status_code == 500
    assert delete_payment_method.json["success"] is False
    assert delete_payment_method.json["location"] == "view delete payment method repo"


# the rest of repo done by auth
# view not 100% from repo error