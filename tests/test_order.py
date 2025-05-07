from models.order import CartItem
from models.product import Product, Promotion
# uv run pytest -v -s --cov=.
# uv run pytest tests/test_order.py -v -s --cov=. --cov-report term-missing

# change test for out of stock to the new one for both inactive and out of stock?


# ---------------------------------------------------------------------------- Get cart test ----------------------------------------------------------------------------

def test_get_cart(client, mock_user_data, mock_token_data, roles_data_inject):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    get_cart = client.get("/order/cart", headers=mock_token_data)

    assert get_cart.status_code == 200
    assert get_cart.json["success"] is True
    assert len(get_cart.json["cart_items"]) == 0


# ---------------------------------------------------------------------------- Add to cart test ----------------------------------------------------------------------------


def test_add_to_cart(
    client,
    mock_user_data,
    mock_token_data,
    mock_add_cart_item,
    products_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    add_to_cart = client.post("/order/cart/item", json=mock_add_cart_item, headers=mock_token_data)

    assert add_to_cart.status_code == 201
    assert add_to_cart.json["success"] is True
    assert add_to_cart.json["message"] == "Item added to cart successfully"
    assert add_to_cart.json["cart_item"]["product_id"] == 1
    assert add_to_cart.json["cart_item"]["quantity"] == 1

    # add to cart again
    add_to_cart = client.post("/order/cart/item", json=mock_add_cart_item, headers=mock_token_data)

    assert add_to_cart.status_code == 201
    assert add_to_cart.json["success"] is True
    assert add_to_cart.json["message"] == "Item added to cart successfully"
    assert add_to_cart.json["cart_item"]["product_id"] == 1
    assert add_to_cart.json["cart_item"]["quantity"] == 2


def test_add_to_cart_product_id_validation_error(
    client, mock_user_data, mock_token_data, mock_add_cart_item, roles_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_add_cart_item["product_id"] = -1

    add_to_cart = client.post("/order/cart/item", json=mock_add_cart_item, headers=mock_token_data)

    assert add_to_cart.status_code == 400
    assert add_to_cart.json["success"] is False
    assert add_to_cart.json["location"] == "view add item to cart request validation"


def test_add_to_cart_quantity_validation_error(
    client, mock_user_data, mock_token_data, mock_add_cart_item, roles_data_inject
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
    client,
    mock_user_data,
    mock_token_data,
    mock_add_cart_item,
    products_data_inject,
    roles_data_inject,
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
    client,
    mock_user_data,
    mock_token_data,
    mock_add_cart_item,
    products_data_inject,
    roles_data_inject,
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
    client,
    mock_user_data,
    mock_token_data,
    mock_update_cart_item,
    products_data_inject,
    cart_item_data_inject,
    roles_data_inject,
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
    client, mock_user_data, mock_token_data, mock_update_cart_item, roles_data_inject
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
    roles_data_inject,
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
    client, mock_user_data, mock_token_data, mock_update_cart_item, roles_data_inject
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


def test_delete_cart_item(
    client,
    mock_user_data,
    mock_token_data,
    products_data_inject,
    cart_item_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    delete_cart_item = client.delete("/order/cart/item/1", headers=mock_token_data)

    assert delete_cart_item.status_code == 200
    assert delete_cart_item.json["success"] is True
    assert delete_cart_item.json["message"] == "Cart item deleted successfully"


def test_delete_cart_repo_error(
    client, mock_user_data, mock_token_data, roles_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    delete_cart_item = client.delete("/order/cart/item/1", headers=mock_token_data)

    assert delete_cart_item.status_code == 500
    assert delete_cart_item.json["success"] is False
    assert delete_cart_item.json["location"] == "view delete item in cart repo"


# ----------------------------------------------------------------------------- Pre-Checkout order test ----------------------------------------------------------------------------


def test_pre_checkout_order_percentage_discount(
    client,
    mock_user_data,
    mock_token_data,
    mock_promotion_data,
    mock_pre_checkout_data,
    cart_data_inject,
    cart_item_data_inject,
    products_data_inject,
    category_data_inject,
    admins_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    create_promotion = client.post(
        "/admin/promotions", json=mock_promotion_data, headers=mock_token_data
    )

    assert create_promotion.status_code == 201

    pre_checkout_order = client.post("/order/pre-checkout", json=mock_pre_checkout_data, headers=mock_token_data)

    promotion = pre_checkout_order.json["promotion"]

    assert pre_checkout_order.status_code == 200
    assert pre_checkout_order.json["success"] is True
    assert len(pre_checkout_order.json) == 3
    assert len(promotion) == 4
    assert len(promotion["eligible_items_ids"]) == 1
    assert promotion["discount"]== "2.20"
    assert promotion["total_price"] == "19.78"


def test_pre_checkout_order_fixed_discount(
    client,
    mock_user_data,
    mock_token_data,
    mock_promotion_data,
    mock_pre_checkout_data,
    cart_data_inject,
    cart_item_data_inject,
    products_data_inject,
    category_data_inject,
    admins_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_promotion_data["promotion_type"] = "fixed_discount"

    create_promotion = client.post(
        "/admin/promotions", json=mock_promotion_data, headers=mock_token_data
    )

    assert create_promotion.status_code == 201

    pre_checkout_order = client.post(
        "/order/pre-checkout", json=mock_pre_checkout_data, headers=mock_token_data
    )

    promotion = pre_checkout_order.json["promotion"]

    assert pre_checkout_order.status_code == 200
    assert pre_checkout_order.json["success"] is True
    assert len(pre_checkout_order.json) == 3
    assert len(promotion) == 4
    assert len(promotion["eligible_items_ids"]) == 1
    assert promotion["discount"] == "10.00"
    assert promotion["total_price"] == "11.98"


def test_pre_checkout_order_promotion_not_active(
    client,
    mock_user_data,
    mock_token_data,
    mock_promotion_data,
    mock_pre_checkout_data,
    cart_data_inject,
    cart_item_data_inject,
    products_data_inject,
    category_data_inject,
    admins_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_promotion_data["end_date"] = "2002-01-01"

    create_promotion = client.post(
        "/admin/promotions", json=mock_promotion_data, headers=mock_token_data
    )

    assert create_promotion.status_code == 201

    pre_checkout_order = client.post(
        "/order/pre-checkout", json=mock_pre_checkout_data, headers=mock_token_data
    )

    promotion = pre_checkout_order.json["promotion"]

    assert pre_checkout_order.status_code == 200
    assert pre_checkout_order.json["success"] is True
    assert pre_checkout_order.json["message"] == "Promotion not active"
    assert promotion["total_price"] == "21.98"
    


def test_pre_checkout_order_promotion_no_eligible_items(
    client,
    mock_user_data,
    mock_token_data,
    mock_promotion_data,
    mock_pre_checkout_data,
    cart_data_inject,
    cart_item_data_inject,
    products_data_inject,
    category_data_inject,
    admins_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_promotion_data["product_ids"] = None
    mock_promotion_data["category_names"] = None

    create_promotion = client.post(
        "/admin/promotions", json=mock_promotion_data, headers=mock_token_data
    )

    assert create_promotion.status_code == 201

    pre_checkout_order = client.post(
        "/order/pre-checkout", json=mock_pre_checkout_data, headers=mock_token_data
    )

    promotion = pre_checkout_order.json["promotion"]

    assert pre_checkout_order.status_code == 200
    assert pre_checkout_order.json["success"] is True
    assert pre_checkout_order.json["message"] == "No eligible items in cart"
    assert promotion["total_price"] == "21.98"


def test_pre_checkout_repo_error(
    client,
    mock_user_data,
    mock_token_data,
    mock_promotion_data,
    mock_pre_checkout_data,
    cart_data_inject,
    cart_item_data_inject,
    products_data_inject,
    category_data_inject,
    admins_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_promotion_data["product_ids"] = None
    mock_promotion_data["category_names"] = None

    pre_checkout_order = client.post(
        "/order/pre-checkout", json=mock_pre_checkout_data, headers=mock_token_data
    )

    assert pre_checkout_order.status_code == 500
    assert pre_checkout_order.json["success"] is False
    assert pre_checkout_order.json["location"] == "view pre-checkout order repo"


# --------------------------------------------------------------- test checkout order ---------------------------------------------------------------


def test_checkout_order_percentage_discount(
    client,
    mock_user_data,
    mock_token_data,
    mock_promotion_data,
    mock_checkout_data,
    cart_data_inject,
    cart_item_data_inject,
    products_data_inject,
    category_data_inject,
    admins_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    create_promotion = client.post(
        "/admin/promotions", json=mock_promotion_data, headers=mock_token_data
    )

    assert create_promotion.status_code == 201

    checkout_order = client.post(
        "/order/checkout", json=mock_checkout_data, headers=mock_token_data
    )
    
    order = checkout_order.json["order"]
    promotion = checkout_order.json["applied_promotion"]

    assert checkout_order.status_code == 201
    assert checkout_order.json["success"] is True
    assert len(checkout_order.json) == 4

    assert len(promotion) == 3
    assert len(promotion["eligible_items_ids"]) == 1
    assert promotion["discount"]== "2.20"

    assert len(order) == 7
    assert order["total_amount"] == 19.78


def test_checkout_order_fixed_discount(
    client,
    mock_user_data,
    mock_token_data,
    mock_promotion_data,
    mock_checkout_data,
    cart_data_inject,
    cart_item_data_inject,
    products_data_inject,
    category_data_inject,
    admins_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_promotion_data["promotion_type"] = "fixed_discount"

    create_promotion = client.post(
        "/admin/promotions", json=mock_promotion_data, headers=mock_token_data
    )

    assert create_promotion.status_code == 201

    checkout_order = client.post(
        "/order/checkout", json=mock_checkout_data, headers=mock_token_data
    )

    order = checkout_order.json["order"]
    promotion = checkout_order.json["applied_promotion"]

    assert checkout_order.status_code == 201
    assert checkout_order.json["success"] is True
    assert len(checkout_order.json) == 4

    assert len(promotion) == 3
    assert len(promotion["eligible_items_ids"]) == 1
    assert promotion["discount"] == "10.00"

    assert len(order) == 7
    assert order["total_amount"] == 11.98


def test_checkout_order_not_enough_stock(
    client,
    mock_user_data,
    mock_token_data,
    mock_promotion_data,
    mock_checkout_data,
    cart_data_inject,
    cart_item_data_inject,
    products_data_inject,
    category_data_inject,
    admins_data_inject,
    roles_data_inject,
    db,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_promotion_data["promotion_type"] = "fixed_discount"

    # update cart item quantity
    cart_item = db.session.execute(db.select(CartItem).filter_by(id = 1)).scalar_one()

    cart_item.quantity = 20

    db.session.commit()

    # run
    create_promotion = client.post(
        "/admin/promotions", json=mock_promotion_data, headers=mock_token_data
    )

    assert create_promotion.status_code == 201

    checkout_order = client.post(
        "/order/checkout", json=mock_checkout_data, headers=mock_token_data
    )

    assert checkout_order.status_code == 400
    assert checkout_order.json["success"] is False
    assert checkout_order.json["issue"] == "Not enough stock"


def test_checkout_order_product_inactive(
    client,
    mock_user_data,
    mock_token_data,
    mock_promotion_data,
    mock_checkout_data,
    cart_data_inject,
    cart_item_data_inject,
    products_data_inject,
    category_data_inject,
    admins_data_inject,
    roles_data_inject,
    db
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_promotion_data["promotion_type"] = "fixed_discount"

    # update cart item quantity
    product = db.session.execute(db.select(Product).filter_by(id=1)).scalar_one()

    product.is_active = False

    db.session.commit()

    # run
    create_promotion = client.post(
        "/admin/promotions", json=mock_promotion_data, headers=mock_token_data
    )

    assert create_promotion.status_code == 201

    checkout_order = client.post(
        "/order/checkout", json=mock_checkout_data, headers=mock_token_data
    )

    assert checkout_order.status_code == 400
    assert checkout_order.json["success"] is False
    assert checkout_order.json["issue"] == "Product is inactive"


def test_checkout_order_usage_limit_reached(
    client,
    mock_user_data,
    mock_token_data,
    mock_promotion_data,
    mock_checkout_data,
    cart_data_inject,
    cart_item_data_inject,
    products_data_inject,
    category_data_inject,
    admins_data_inject,
    roles_data_inject,
    db
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    create_promotion = client.post(
        "/admin/promotions", json=mock_promotion_data, headers=mock_token_data
    )

    assert create_promotion.status_code == 201

    # Set promotion usage limit to 0
    promotion = db.session.execute(
        db.select(Promotion).filter_by(id=1)
    ).scalar_one()

    promotion.usage_limit = 0

    db.session.commit()

    # Checkout order
    checkout_order = client.post(
        "/order/checkout", json=mock_checkout_data, headers=mock_token_data
    )

    assert checkout_order.status_code == 400
    assert checkout_order.json["success"] is False
    assert checkout_order.json["message"] == "Promo usage limit reached"
    assert checkout_order.json["location"] == "view checkout order repo"


def test_checkout_order_shipping_address_validation_error(
    client,
    mock_user_data,
    mock_token_data,
    mock_promotion_data,
    mock_checkout_data,
    cart_data_inject,
    cart_item_data_inject,
    products_data_inject,
    category_data_inject,
    admins_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    create_promotion = client.post(
        "/admin/promotions", json=mock_promotion_data, headers=mock_token_data
    )

    assert create_promotion.status_code == 201

    mock_checkout_data["shipping_address_id"] = -1

    checkout_order = client.post(
        "/order/checkout", json=mock_checkout_data, headers=mock_token_data
    )

    assert checkout_order.status_code == 400
    assert checkout_order.json["success"] is False
    assert checkout_order.json["location"] == "view checkout order request validation"


def test_checkout_order_payment_method_validation_error(
    client,
    mock_user_data,
    mock_token_data,
    mock_promotion_data,
    mock_checkout_data,
    cart_data_inject,
    cart_item_data_inject,
    products_data_inject,
    category_data_inject,
    admins_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    create_promotion = client.post(
        "/admin/promotions", json=mock_promotion_data, headers=mock_token_data
    )

    assert create_promotion.status_code == 201

    mock_checkout_data["payment_method_id"] = -1

    checkout_order = client.post(
        "/order/checkout", json=mock_checkout_data, headers=mock_token_data
    )

    assert checkout_order.status_code == 400
    assert checkout_order.json["success"] is False
    assert checkout_order.json["location"] == "view checkout order request validation"


def test_checkout_order_repo_error(
    client,
    mock_user_data,
    mock_token_data,
    mock_promotion_data,
    mock_checkout_data,
    cart_data_inject,
    cart_item_data_inject,
    products_data_inject,
    category_data_inject,
    admins_data_inject,
    roles_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    checkout_order = client.post(
        "/order/checkout", json=mock_checkout_data, headers=mock_token_data
    )

    assert checkout_order.status_code == 500
    assert checkout_order.json["success"] is False
    assert checkout_order.json["location"] == "view checkout order repo"


# ---------------------------------------------------------------------------- Get order test ----------------------------------------------------------------------------


def test_get_order(client, mock_user_data, mock_token_data, roles_data_inject, order_data_inject):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    get_order = client.get("/order/1234567890", headers=mock_token_data)
    
    assert get_order.status_code == 200
    assert get_order.json["success"] is True
    assert len(get_order.json["order"] ) == 7


def test_get_order_repo_error(
    client, mock_user_data, mock_token_data, roles_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    get_order = client.get("/order/1234567890", headers=mock_token_data)

    assert get_order.status_code == 500
    assert get_order.json["success"] is False
    assert get_order.json["location"] == "view get order repo"


# ---------------------------------------------------------------------------- Update orders test ----------------------------------------------------------------------------


def test_update_order(
    client, mock_user_data, mock_token_data, mock_update_order_data, roles_data_inject, order_data_inject
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    update_order = client.put("/order/1234567890",json=mock_update_order_data, headers=mock_token_data)

    assert update_order.status_code == 200
    assert update_order.json["success"] is True
    assert update_order.json["message"] == "Order status updated successfully"
    assert len(update_order.json["order"] ) == 7
    assert update_order.json["order"]["status"] == mock_update_order_data["status"]


def test_update_order_status_validation_error(
    client,
    mock_user_data,
    mock_token_data,
    mock_update_order_data,
    roles_data_inject,
    order_data_inject,
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    mock_update_order_data["status"] = ""

    update_order = client.put(
        "/order/1234567890", json=mock_update_order_data, headers=mock_token_data
    )

    assert update_order.status_code == 400
    assert update_order.json["success"] is False
    assert (
        update_order.json["location"] == "view update order status request validation"
    )


def test_update_order_repo_error(
    client,
    mock_user_data,
    mock_token_data,
    mock_update_order_data,
    roles_data_inject,

):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    update_order = client.put(
        "/order/1234567890", json=mock_update_order_data, headers=mock_token_data
    )

    assert update_order.status_code == 500
    assert update_order.json["success"] is False
    assert update_order.json["location"] == "view update order status repo"


# ---------------------------------------------------------------------------- Get order test ----------------------------------------------------------------------------


def test_get_all_orders(client, mock_user_data, mock_token_data, roles_data_inject, order_data_inject):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    get_all_orders = client.get("/order", headers=mock_token_data)

    assert get_all_orders.status_code == 200
    assert get_all_orders.json["success"] is True
    assert len(get_all_orders.json["orders"]) == 1
    assert len(get_all_orders.json["orders"][0]) == 7




# views\order.py               137      9    93%   31-33, 413-415
# error 500

# schemas\order.py              89      0   100%

# router\order.py               40      0   100%

# repo\order.py                104      0   100%

# models\order.py               55      0   100%