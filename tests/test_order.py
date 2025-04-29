
# uv run pytest -v -s --cov=.
# uv run pytest tests/test_order.py -v -s --cov=.


# ---------------------------------------------------------------------------- Get cart test ----------------------------------------------------------------------------

def test_get_cart(client, mock_user_data, mock_token_data):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    get_cart = client.get("/order/cart", headers=mock_token_data)

    assert get_cart.status_code == 200
    assert get_cart.json["success"] is True
    assert len(get_cart.json["cart_items"]) == 0


# ---------------------------------------------------------------------------- Add to cart test ----------------------------------------------------------------------------


def test_add_to_cart(client, mock_user_data, mock_token_data ,mock_add_cart_item, products_data_inject):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    add_to_cart = client.post("/order/cart/item", json=mock_add_cart_item, headers=mock_token_data)

    assert add_to_cart.status_code == 201
    assert add_to_cart.json["success"] is True
    assert add_to_cart.json["message"] == "Item added to cart successfully"
    assert add_to_cart.json["cart_item"]["product_id"] == 1
    assert add_to_cart.json["cart_item"]["quantity"] == 1


def test_add_to_cart_product_id_validation_error(client, mock_user_data, mock_token_data, mock_add_cart_item):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_add_cart_item["product_id"] = -1

    add_to_cart = client.post("/order/cart/item", json=mock_add_cart_item, headers=mock_token_data)

    assert add_to_cart.status_code == 400
    assert add_to_cart.json["success"] is False
    assert add_to_cart.json["location"] == "view add item to cart request validation"


def test_add_to_cart_quantity_validation_error(
    client, mock_user_data, mock_token_data, mock_add_cart_item
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_add_cart_item["quantity"] = -1

    add_to_cart = client.post(
        "/order/cart/item", json=mock_add_cart_item, headers=mock_token_data
    )

    assert add_to_cart.status_code == 400
    assert add_to_cart.json["success"] is False
    assert add_to_cart.json["location"] == "view add item to cart request validation"


def test_add_to_cart_out_of_stock(
    client, mock_user_data, mock_token_data, mock_add_cart_item, products_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_add_cart_item["quantity"] = 100

    add_to_cart = client.post(
        "/order/cart/item", json=mock_add_cart_item, headers=mock_token_data
    )

    assert add_to_cart.status_code == 400
    assert add_to_cart.json["success"] is False
    assert add_to_cart.json["message"] == "Not enough stock"


def test_add_to_cart_repo_error(
    client, mock_user_data, mock_token_data, mock_add_cart_item, products_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_add_cart_item["product_id"] = 100

    add_to_cart = client.post(
        "/order/cart/item", json=mock_add_cart_item, headers=mock_token_data
    )

    assert add_to_cart.status_code == 500
    assert add_to_cart.json["success"] is False
    assert add_to_cart.json["location"] == "view add item to cart repo"


# ---------------------------------------------------------------------------- update cart item test ----------------------------------------------------------------------------


def test_update_cart_item(
    client, mock_user_data, mock_token_data, mock_update_cart_item, products_data_inject, cart_item_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    update_cart_item = client.put(
        "/order/cart/item/1", json=mock_update_cart_item, headers=mock_token_data
    )

    assert update_cart_item.status_code == 200
    assert update_cart_item.json["success"] is True
    assert update_cart_item.json["message"] == "Cart item updated successfully"
    assert update_cart_item.json["cart_item"]["product_id"] == 1
    assert update_cart_item.json["cart_item"]["quantity"] == 5


def test_update_cart_item_quantity_validation_error(
    client,
    mock_user_data,
    mock_token_data,
    mock_update_cart_item,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_update_cart_item["quantity"] = -1

    update_cart_item = client.put(
        "/order/cart/item/1", json=mock_update_cart_item, headers=mock_token_data
    )

    assert update_cart_item.status_code == 400
    assert update_cart_item.json["success"] is False
    assert (
        update_cart_item.json["location"] == "view update item in cart request validation"
    )


def test_update_cart_item_out_of_stock(
    client,
    mock_user_data,
    mock_token_data,
    mock_update_cart_item,
    products_data_inject,
    cart_item_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_update_cart_item["quantity"] = 100

    update_cart_item = client.put(
        "/order/cart/item/1", json=mock_update_cart_item, headers=mock_token_data
    )

    assert update_cart_item.status_code == 400
    assert update_cart_item.json["success"] is False
    assert update_cart_item.json["message"] == "Not enough stock"


def test_update_cart_repo_error(
    client,
    mock_user_data,
    mock_token_data,
    mock_update_cart_item,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_update_cart_item["quantity"] = 100

    update_cart_item = client.put(
        "/order/cart/item/1", json=mock_update_cart_item, headers=mock_token_data
    )

    assert update_cart_item.status_code == 500
    assert update_cart_item.json["success"] is False
    assert update_cart_item.json["location"] == "view update item in cart repo"


# ---------------------------------------------------------------------------- delete cart item test ----------------------------------------------------------------------------


def test_delete_cart_item(client, mock_user_data, mock_token_data, products_data_inject, cart_item_data_inject):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    delete_cart_item = client.delete("/order/cart/item/1", headers=mock_token_data)

    assert delete_cart_item.status_code == 200
    assert delete_cart_item.json["success"] is True
    assert delete_cart_item.json["message"] == "Cart item deleted successfully"


def test_delete_cart_repo_error(client, mock_user_data, mock_token_data):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    delete_cart_item = client.delete("/order/cart/item/1", headers=mock_token_data)

    assert delete_cart_item.status_code == 500
    assert delete_cart_item.json["success"] is False
    assert delete_cart_item.json["location"] == "view delete item in cart repo"
