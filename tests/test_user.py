import models

# uv run pytest -v -s --cov=.
# uv run pytest tests/test_user.py -v -s --cov=.

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
    client, mock_user_data, mock_token_data, mock_update_user_data, db
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
    client, mock_user_data, mock_token_data, mock_update_user_data
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
    client, mock_user_data, mock_token_data, mock_update_user_data
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


def test_update_user_image_url_validation_error(
    client, mock_user_data, mock_token_data, mock_update_user_data
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_update_user_data["profile_image_url"] = "test"

    update_user = client.put(
        "/user/me", json=mock_update_user_data, headers=mock_token_data
    )

    assert update_user.status_code == 400
    assert update_user.json["success"] is False
    assert update_user.json["location"] == "view update user profile request validation"


def test_update_user_password_validation_error(
    client, mock_user_data, mock_token_data, mock_update_user_data
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
