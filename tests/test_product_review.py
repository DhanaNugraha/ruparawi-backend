# uv run pytest -v -s --cov=.
# uv run pytest tests/test_product_review.py -v -s --cov=. --cov-report term-missing


# ---------------------------------------------------------------------------- Product Review Tests ----------------------------------------------------------------------------


def test_create_product_review(
    client,
    mock_product_review_data,
    mock_token_data,
    mock_user_data,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    product_review = client.post(
        "/review", json=mock_product_review_data, headers=mock_token_data
    )

    assert product_review.status_code == 201
    assert (
        set(product_review.json.values()) & set(mock_product_review_data.values())
    ) == set(mock_product_review_data.values())


# ---------------------------------------------------------------------------- Get Product Review Tests ----------------------------------------------------------------------------


def test_get_product_review_by_product_id(
    client,
    mock_product_review_data,
    mock_token_data,
    mock_user_data,
    roles_data_inject,
    product_review_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    product_review = client.get("/review/product/1", headers=mock_token_data)

    assert product_review.status_code == 200
    assert len(product_review.json) == 1
    assert len(product_review.json[0]) == 5


def test_get_product_review_by_review_id(
    client,
    mock_product_review_data,
    mock_token_data,
    mock_user_data,
    roles_data_inject,
    product_review_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    product_review = client.get("/review/1", headers=mock_token_data)

    assert product_review.status_code == 200
    assert len(product_review.json) == 5


def test_get_product_review_by_review_id_not_found(
    client,
    mock_product_review_data,
    mock_token_data,
    mock_user_data,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    product_review = client.get("/review/1", headers=mock_token_data)

    assert product_review.status_code == 404
    assert product_review.json["error"] == "Review not found"


# ---------------------------------------------------------------------------- Edit Product Review Tests ----------------------------------------------------------------------------


def test_edit_product_review_by_id(
    client,
    mock_product_review_data,
    mock_token_data,
    mock_user_data,
    roles_data_inject,
    product_review_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    product_review = client.put(
        "/review/1/edit", json=mock_product_review_data, headers=mock_token_data
    )

    assert product_review.status_code == 200
    assert (
        set(product_review.json.values()) & set(mock_product_review_data.values())
    ) == set(mock_product_review_data.values())
    assert len(product_review.json) == 5


def test_edit_product_review_by_id_not_found(
    client,
    mock_product_review_data,
    mock_token_data,
    mock_user_data,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    product_review = client.put(
        "/review/1/edit", json=mock_product_review_data, headers=mock_token_data
    )

    assert product_review.status_code == 404
    assert product_review.json["error"] == "Review not found"


# ---------------------------------------------------------------------------- Delete Product Review Tests ----------------------------------------------------------------------------


def test_delete_product_review_by_id(
    client,
    mock_product_review_data,
    mock_token_data,
    mock_user_data,
    roles_data_inject,
    product_review_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    product_review = client.delete("/review/1/delete", headers=mock_token_data)

    assert product_review.status_code == 200
    assert product_review.json["message"] == "Review deleted successfully"


def test_delete_product_review_by_id_not_found(
    client,
    mock_product_review_data,
    mock_token_data,
    mock_user_data,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    product_review = client.delete("/review/1/delete", headers=mock_token_data)

    assert product_review.status_code == 404
    assert product_review.json["error"] == "Review not found"



# router\product_review.py          35      0   100%
# repo\product_review.py            26      0   100%
