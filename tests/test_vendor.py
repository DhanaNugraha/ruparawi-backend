import models

# uv run pytest -v -s --cov=.
# uv run pytest tests/test_vendor.py -v -s --cov=.

# ---------------------------------------------------------------------------- Admin apply test ----------------------------------------------------------------------------


def test_vendor_apply(client, test_app, mock_user_data, mock_vendor_apply_data, mock_token_data):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    apply_vendor = client.post("/vendor/apply", json=mock_vendor_apply_data, headers=mock_token_data)

    assert apply_vendor.status_code == 201


# test vendor not approved in auth auth

# testing validation error

