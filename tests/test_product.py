import models

# uv run pytest -v -s --cov=.
# uv run pytest tests/test_product.py -v -s --cov=.


# ---------------------------------------------------------------------------- Create product Tests ----------------------------------------------------------------------------


def test_create_product(
    client, mock_create_product_data, mock_vendor_token_data, mock_vendor_data, db
):
    register_vendor = client.post("/auth/register", json=mock_vendor_data)

    assert register_vendor.status_code == 201

    product = client.post(
        "/products", json=mock_create_product_data, headers=mock_vendor_token_data
    )

    assert product.status_code == 201
    assert product.json["success"] is True
    assert product.json["message"] == "Product created successfully"
    assert product.json["product"]["name"] == mock_create_product_data["name"]

    tags = db.session.execute(db.select(models.ProductTag)).scalars().all()
    sustainability_attributes = (
        db.session.execute(db.select(models.SustainabilityAttribute)).scalars().all()
    )

    assert len(tags) == 2
    assert len(sustainability_attributes) == 2


def test_create_product_not_vendor(
    client, mock_create_product_data, mock_token_data, mock_user_data
):
    register_user = client.post("/auth/register", json=mock_user_data)

    assert register_user.status_code == 201

    product = client.post(
        "/products", json=mock_create_product_data, headers=mock_token_data
    )

    assert product.status_code == 403
    assert product.json["success"] is False
    assert product.json["location"] == "view create product vendor validation"
    assert product.json["message"] == "User is not a vendor"


def test_create_product_name_validation_error(
    client, mock_create_product_data, mock_vendor_token_data, mock_vendor_data
):
    register_vendor = client.post("/auth/register", json=mock_vendor_data)

    assert register_vendor.status_code == 201

    mock_create_product_data["name"] = ""

    product = client.post(
        "/products", json=mock_create_product_data, headers=mock_vendor_token_data
    )

    assert product.status_code == 400
    assert product.json["success"] is False
    assert product.json["location"] == "view create product request validation"


def test_create_product_description_validation_error(
    client, mock_create_product_data, mock_vendor_token_data, mock_vendor_data
):
    register_vendor = client.post("/auth/register", json=mock_vendor_data)

    assert register_vendor.status_code == 201

    mock_create_product_data["description"] = ""

    product = client.post(
        "/products", json=mock_create_product_data, headers=mock_vendor_token_data
    )

    assert product.status_code == 400
    assert product.json["success"] is False
    assert product.json["location"] == "view create product request validation"


def test_create_product_price_validation_error(
    client, mock_create_product_data, mock_vendor_token_data, mock_vendor_data
):
    register_vendor = client.post("/auth/register", json=mock_vendor_data)

    assert register_vendor.status_code == 201

    mock_create_product_data["price"] = -1

    product = client.post(
        "/products", json=mock_create_product_data, headers=mock_vendor_token_data
    )

    assert product.status_code == 400
    assert product.json["success"] is False
    assert product.json["location"] == "view create product request validation"


def test_create_product_tags_validation_error(
    client, mock_create_product_data, mock_vendor_token_data, mock_vendor_data
):
    register_vendor = client.post("/auth/register", json=mock_vendor_data)

    assert register_vendor.status_code == 201

    mock_create_product_data["tags"] = [i for i in ("a" * 15)]

    product = client.post(
        "/products", json=mock_create_product_data, headers=mock_vendor_token_data
    )

    assert product.status_code == 400
    assert product.json["success"] is False
    assert product.json["location"] == "view create product request validation"


def test_create_product_sustainability_attributes_validation_error(
    client, mock_create_product_data, mock_vendor_token_data, mock_vendor_data
):
    register_vendor = client.post("/auth/register", json=mock_vendor_data)

    assert register_vendor.status_code == 201

    mock_create_product_data["sustainability_attributes"] = [i for i in ("a" * 10)]

    product = client.post(
        "/products", json=mock_create_product_data, headers=mock_vendor_token_data
    )

    assert product.status_code == 400
    assert product.json["success"] is False
    assert product.json["location"] == "view create product request validation"


def test_create_product_stock_validation_error(
    client, mock_create_product_data, mock_vendor_token_data, mock_vendor_data
):
    register_vendor = client.post("/auth/register", json=mock_vendor_data)

    assert register_vendor.status_code == 201

    mock_create_product_data["stock_quantity"] = -1

    product = client.post(
        "/products", json=mock_create_product_data, headers=mock_vendor_token_data
    )

    assert product.status_code == 400
    assert product.json["success"] is False
    assert product.json["location"] == "view create product request validation"


def test_create_product_order_quantity_validation_error(
    client, mock_create_product_data, mock_vendor_token_data, mock_vendor_data
):
    register_vendor = client.post("/auth/register", json=mock_vendor_data)

    assert register_vendor.status_code == 201

    mock_create_product_data["min_order_quantity"] = 0

    product = client.post(
        "/products", json=mock_create_product_data, headers=mock_vendor_token_data
    )

    assert product.status_code == 400
    assert product.json["success"] is False
    assert product.json["location"] == "view create product request validation"


# ---------------------------------------------------------------------------- Get product Tests ----------------------------------------------------------------------------


def test_get_all_product(client, products_data_inject):
    product = client.get("/products")

    assert product.status_code == 200
    assert product.json["success"] is True
    assert len(product.json["products"]) == 2


def test_get_product_with_args(
    client, mock_multiple_create_product_data, mock_vendor_token_data, mock_vendor_data
):
    # register vendor
    register_vendor = client.post("/auth/register", json=mock_vendor_data)
    assert register_vendor.status_code == 201

    # insert product
    for product in mock_multiple_create_product_data:
        product = client.post("/products", json=product, headers=mock_vendor_token_data)

        assert product.status_code == 201

    # get product
    product = client.get(
        "/products?min_price=10&page=1&per_page=20&max_price=30&tags=eco-friendly&tags=handmade&category_id=1"
    )

    assert product.status_code == 200
    assert product.json["success"] is True
    assert len(product.json["products"]) == 1
    assert product.json["pagination"]["total"] == 1


def test_get_product_invalid_args(client):
    product = client.get("/products?min_price=-1")

    assert product.status_code == 400
    assert product.json["success"] is False
    assert product.json["location"] == "view list products request validation"

    product = client.get("/products?max_price=-1")

    assert product.status_code == 400
    assert product.json["success"] is False
    assert product.json["location"] == "view list products request validation"


# ---------------------------------------------------------------------------- Get product details Tests ----------------------------------------------------------------------------


def test_get_product_details(client, products_data_inject):
    product = client.get("/products/1")

    assert product.status_code == 200
    assert product.json["success"] is True
    assert product.json["product"]["id"] == 1
    assert len(product.json["product"]) == 14


# ---------------------------------------------------------------------------- Update product details Tests ----------------------------------------------------------------------------


def test_update_product_details(
    client,
    mock_update_product_data,
    mock_vendor_token_data,
    mock_vendor_data,
    db,
    products_data_inject,
):
    register_vendor = client.post("/auth/register", json=mock_vendor_data)

    assert register_vendor.status_code == 201

    product = client.put(
        "/products/1", json=mock_update_product_data, headers=mock_vendor_token_data
    )

    assert product.status_code == 200
    assert product.json["success"] is True
    assert product.json["message"] == "Product updated successfully"
    assert product.json["product"]["name"] == mock_update_product_data["name"]

    tags = db.session.execute(db.select(models.ProductTag)).scalars().all()

    sustainability_attributes = (
        db.session.execute(db.select(models.SustainabilityAttribute)).scalars().all()
    )

    assert len(tags) == 2
    assert len(sustainability_attributes) == 2


def test_update_product_name_validation_error(
    client, mock_update_product_data, mock_vendor_token_data, mock_vendor_data
):
    register_vendor = client.post("/auth/register", json=mock_vendor_data)

    assert register_vendor.status_code == 201

    mock_update_product_data["name"] = ""

    product = client.put(
        "/products/1", json=mock_update_product_data, headers=mock_vendor_token_data
    )

    assert product.status_code == 400
    assert product.json["success"] is False
    assert product.json["location"] == "view update product request validation"


def test_update_product_description_validation_error(
    client, mock_update_product_data, mock_vendor_token_data, mock_vendor_data
):
    register_vendor = client.post("/auth/register", json=mock_vendor_data)

    assert register_vendor.status_code == 201

    mock_update_product_data["description"] = ""

    product = client.put(
        "/products/1", json=mock_update_product_data, headers=mock_vendor_token_data
    )

    assert product.status_code == 400
    assert product.json["success"] is False
    assert product.json["location"] == "view update product request validation"


def test_update_product_price_validation_error(
    client, mock_update_product_data, mock_vendor_token_data, mock_vendor_data
):
    register_vendor = client.post("/auth/register", json=mock_vendor_data)

    assert register_vendor.status_code == 201

    mock_update_product_data["price"] = -1

    product = client.put(
        "/products/1", json=mock_update_product_data, headers=mock_vendor_token_data
    )

    assert product.status_code == 400
    assert product.json["success"] is False
    assert product.json["location"] == "view update product request validation"


def test_update_product_tags_validation_error(
    client, mock_update_product_data, mock_vendor_token_data, mock_vendor_data
):
    register_vendor = client.post("/auth/register", json=mock_vendor_data)

    assert register_vendor.status_code == 201

    mock_update_product_data["tags"] = [i for i in ("a" * 15)]

    product = client.put(
        "/products/1", json=mock_update_product_data, headers=mock_vendor_token_data
    )

    assert product.status_code == 400
    assert product.json["success"] is False
    assert product.json["location"] == "view update product request validation"


def test_update_product_sustainability_attributes_validation_error(
    client, mock_update_product_data, mock_vendor_token_data, mock_vendor_data
):
    register_vendor = client.post("/auth/register", json=mock_vendor_data)

    assert register_vendor.status_code == 201

    mock_update_product_data["sustainability_attributes"] = [i for i in ("a" * 10)]

    product = client.put(
        "/products/1", json=mock_update_product_data, headers=mock_vendor_token_data
    )

    assert product.status_code == 400
    assert product.json["success"] is False
    assert product.json["location"] == "view update product request validation"


def test_update_product_stock_validation_error(
    client, mock_update_product_data, mock_vendor_token_data, mock_vendor_data
):
    register_vendor = client.post("/auth/register", json=mock_vendor_data)

    assert register_vendor.status_code == 201

    mock_update_product_data["stock_quantity"] = -1

    product = client.put(
        "/products/1", json=mock_update_product_data, headers=mock_vendor_token_data
    )

    assert product.status_code == 400
    assert product.json["success"] is False
    assert product.json["location"] == "view update product request validation"


def test_update_product_order_quantity_validation_error(
    client, mock_update_product_data, mock_vendor_token_data, mock_vendor_data
):
    register_vendor = client.post("/auth/register", json=mock_vendor_data)

    assert register_vendor.status_code == 201

    mock_update_product_data["min_order_quantity"] = 0

    product = client.put(
        "/products/1", json=mock_update_product_data, headers=mock_vendor_token_data
    )

    assert product.status_code == 400
    assert product.json["success"] is False
    assert product.json["location"] == "view update product request validation"


def test_update_product_not_vendor(
    client, mock_update_product_data, mock_vendor_token_data, mock_vendor_data
):
    register_vendor = client.post("/auth/register", json=mock_vendor_data)

    assert register_vendor.status_code == 201

    product = client.put(
        "/products/2", json=mock_update_product_data, headers=mock_vendor_token_data
    )

    assert product.status_code == 500
    assert product.json["success"] is False
    assert product.json["location"] == "view update product repo"


# ----------------------------------------------------------------------------  Delete product test ----------------------------------------------------------------------------

def test_delete_product(client, mock_vendor_token_data, mock_vendor_data, products_data_inject):
    register_vendor = client.post("/auth/register", json=mock_vendor_data)

    assert register_vendor.status_code == 201

    product = client.delete("/products/1", headers=mock_vendor_token_data)

    assert product.status_code == 200
    assert product.json["success"] is True
    assert product.json["message"] == "Product soft deleted (archived) successfully"
    assert product.json["product"]["name"] == "Product 1"
    assert product.json["product"]["is_active"] is False


def test_delete_product_not_vendor(client, mock_vendor_token_data, mock_vendor_data, products_data_inject):
    register_vendor = client.post("/auth/register", json=mock_vendor_data)

    assert register_vendor.status_code == 201

    product = client.delete("/products/2", headers=mock_vendor_token_data)

    assert product.status_code == 403
    assert product.json["success"] is False
    assert product.json["message"] == "You are not authorized to delete this product"


