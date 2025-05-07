# test with products and review inject
# test route /task-status

# uv run pytest -v -s --cov=.
# uv run pytest tests/test_scheduled.py -v -s --cov=. --cov-report term-missing


# ----------------------------------------------------------------------------- test background scheduled jobs ----------------------------------------------------------------------------


def test_scheduled_job(
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

    task_status = client.get("/task-status", headers=mock_token_data)

    assert task_status.status_code == 200
    assert task_status.json["status"] == "running"
