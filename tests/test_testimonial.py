# uv run pytest -v -s --cov=.
# uv run pytest tests/test_testimonial.py -v -s --cov=. --cov-report term-missing


# ---------------------------------------------------------------------------- Testimonial Tests ----------------------------------------------------------------------------


def test_create_testimonial(
    client,
    mock_user_data,
    mock_token_data,
    approved_vendor_profile_inject,
    mock_testimonial_data,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    create_testimonial = client.post(
        "/testimonial", json=mock_testimonial_data, headers=mock_token_data
    )

    assert create_testimonial.status_code == 201
    assert (
        set(create_testimonial.json.values()) & set(mock_testimonial_data.values())
    ) == set(mock_testimonial_data.values())


def test_get_testimonial(
    client,
    mock_user_data,
    mock_token_data,
    approved_vendor_profile_inject,
    mock_testimonial_data,
    roles_data_inject,
    testimonial_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    get_testimonial = client.get("/testimonial")

    assert get_testimonial.status_code == 200
    assert len(get_testimonial.json) == 1
    assert len(get_testimonial.json[0]) == 3


def test_update_testimonial(
    client,
    mock_user_data,
    mock_token_data,
    approved_vendor_profile_inject,
    mock_testimonial_data,
    roles_data_inject,
    testimonial_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    update_testimonial = client.put(
        "/testimonial/1", json=mock_testimonial_data, headers=mock_token_data
    )

    assert update_testimonial.status_code == 200
    assert len(update_testimonial.json) == 2
    assert (
        set(update_testimonial.json.values()) & set(mock_testimonial_data.values())
    ) == set(mock_testimonial_data.values())


def test_update_testimonial_not_found(
    client,
    mock_user_data,
    mock_token_data,
    approved_vendor_profile_inject,
    mock_testimonial_data,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    update_testimonial = client.put(
        "/testimonial/1", json=mock_testimonial_data, headers=mock_token_data
    )

    assert update_testimonial.status_code == 404
    assert update_testimonial.json["error"] == "Testimonial Not found"


def test_delete_testimonial(
    client,
    mock_user_data,
    mock_token_data,
    approved_vendor_profile_inject,
    mock_testimonial_data,
    roles_data_inject,
    testimonial_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    delete_testimonial = client.delete("/testimonial/1", headers=mock_token_data)

    assert delete_testimonial.status_code == 200
    assert delete_testimonial.json["message"] == "Testimonial deleted successfully"


def test_delete_testimonial_not_found(
    client,
    mock_user_data,
    mock_token_data,
    approved_vendor_profile_inject,
    mock_testimonial_data,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    delete_testimonial = client.delete("/testimonial/1", headers=mock_token_data)

    assert delete_testimonial.status_code == 404
    assert delete_testimonial.json["error"] == "Testimonial Not found"


# repo\testimonial.py            23      0   100%
# router\testimonial.py          33      0   100%
