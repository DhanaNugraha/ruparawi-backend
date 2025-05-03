import models

# uv run pytest -v -s --cov=. --cov-report term-missing
# uv run pytest tests/test_auth.py -v -s --cov=. --cov-report term-missing


# ---------------------------------------------------------------------------- Register User Tests ----------------------------------------------------------------------------
def test_register_user(client, db, mock_user_data, users_data_inject, roles_data_inject):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201
    assert register_user.json["success"] is True

    user = db.session.execute(
        db.select(models.User).filter_by(email=mock_user_data["email"])
    ).scalar_one()

    assert user.id == 3
    assert user.username == mock_user_data["username"]
    assert user.email == mock_user_data["email"]
    assert repr([role.name for role in user.role][0]) == "'buyer'"


def test_register_user_username_validation_error(client, mock_user_data):
    # test < 3 characters username
    mock_user_data["username"] = ""
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 400
    assert register_user.json["success"] is False
    assert register_user.json["location"] == "view register user request validation"

    # test non alphanumeric and underscore characters username
    mock_user_data["username"] = "@----@"
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 400
    assert register_user.json["success"] is False
    assert register_user.json["location"] == "view register user request validation"


def test_register_user_password_validation_error(client, mock_user_data):
    # test < 8 characters username
    mock_user_data["password"] = "1234567"
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 400
    assert register_user.json["success"] is False
    assert register_user.json["location"] == "view register user request validation"


def test_register_user_email_validation_error(client, mock_user_data):
    # test empty email
    mock_user_data["email"] = ""
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 400
    assert register_user.json["success"] is False
    assert register_user.json["location"] == "view register user request validation"

    # test invalid email pattern
    mock_user_data["email"] = "invalid_email_pattern"
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 400
    assert register_user.json["success"] is False
    assert register_user.json["location"] == "view register user request validation"

    # test consecutive dots in email
    mock_user_data["email"] = "a@bc..com"
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 400
    assert register_user.json["success"] is False
    assert register_user.json["location"] == "view register user request validation"

    # test email too long
    mock_user_data["email"] = "a" * 256 + "@example.com"
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 400
    assert register_user.json["success"] is False
    assert register_user.json["location"] == "view register user request validation"


def test_register_user_duplicates(client, mock_user_data, users_data_inject):
    # test email already exist
    mock_user_data["email"] = "john.doe@example.com"
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 500
    assert register_user.json["success"] is False
    assert register_user.json["location"] == "view create user repo"

    # test username already exist
    mock_user_data["username"] = "john"
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 500
    assert register_user.json["success"] is False


# ---------------------------------------------------------------------------- Login User Tests ----------------------------------------------------------------------------


def test_login_user(client, db, mock_user_data, mock_login_data, roles_data_inject):
    # register mock user
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    # login to mock user
    login_user = client.post("/auth/login", json=mock_login_data)

    assert login_user.status_code == 200
    assert login_user.json["success"] is True
    assert login_user.json["user"]["email"] == mock_user_data["email"]
    assert login_user.json["user"]["username"] == mock_user_data["username"]


def test_login_user_password_validation_error(client, mock_login_data):
    # test < 8 characters username
    mock_login_data["password"] = "1234567"
    login_user = client.post("/auth/login", json=mock_login_data)

    assert login_user.status_code == 400
    assert login_user.json["success"] is False
    assert login_user.json["location"] == "view login user request validation"


def test_login_user_email_validation_error(client, mock_login_data, users_data_inject):
    # test empty email
    mock_login_data["email"] = ""
    login_user = client.post("/auth/login", json=mock_login_data)

    assert login_user.status_code == 400
    assert login_user.json["success"] is False
    assert login_user.json["location"] == "view login user request validation"

    # test invalid email pattern
    mock_login_data["email"] = "invalid_email_pattern"
    login_user = client.post("/auth/login", json=mock_login_data)

    assert login_user.status_code == 400
    assert login_user.json["success"] is False
    assert login_user.json["location"] == "view login user request validation"

    # test consecutive dots in email
    mock_login_data["email"] = "a@bc..com"
    login_user = client.post("/auth/login", json=mock_login_data)

    assert login_user.status_code == 400
    assert login_user.json["success"] is False
    assert login_user.json["location"] == "view login user request validation"

    # test email too long
    mock_login_data["email"] = "a" * 256 + "@example.com"
    login_user = client.post("/auth/login", json=mock_login_data)

    assert login_user.status_code == 400
    assert login_user.json["success"] is False
    assert login_user.json["location"] == "view login user request validation"


def test_login_user_invalid_credential(client, mock_user_data, mock_login_data, roles_data_inject):
    # register mock user
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    # save correct email for later
    correct_email = mock_user_data["email"]

    # test invalid email
    mock_login_data["email"] = "john.wrong@example.com"
    login_user = client.post("/auth/login", json=mock_login_data)

    assert login_user.status_code == 404

    # test invalid password
    mock_login_data["email"] = correct_email
    mock_login_data["password"] = "wrong_password"
    login_user = client.post("/auth/login", json=mock_login_data)

    assert login_user.status_code == 401
    assert login_user.json["success"] is False
    assert login_user.json["location"] == "view login user repo"


# ---------------------------------------------------------------------------- Get Current User Tests ----------------------------------------------------------------------------


def test_get_current_user(client, mock_user_data, mock_token_data, roles_data_inject):
    # register mock user
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    # get current user
    get_current_user = client.get("/auth/me", headers=mock_token_data)

    assert get_current_user.status_code == 200
    assert get_current_user.json["success"] is True
    assert get_current_user.json["user"]["email"] == mock_user_data["email"]
    assert get_current_user.json["user"]["username"] == mock_user_data["username"]
    assert len(get_current_user.json["user"]) == 10


def test_get_current_user_missing_user(client, mock_token_data):
    # get current user
    get_current_user = client.get("/auth/me", headers=mock_token_data)

    assert get_current_user.status_code == 404


#  ---------------------------------------------------------------------------- refresh token Tests ----------------------------------------------------------------------------

def test_refresh_token(client, mock_user_data, mock_token_data, mock_refresh_token_data, roles_data_inject):
    # register mock user
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    # login user
    login_user = client.post("/auth/login", json=mock_user_data)

    assert login_user.status_code == 200

    # refresh token
    refresh_token = client.post("/auth/refresh", headers=mock_refresh_token_data)

    assert refresh_token.status_code == 200
    assert len(refresh_token.json) == 1


# all 100%