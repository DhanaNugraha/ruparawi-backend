import models

# uv run pytest -v -s --cov=.
# uv run pytest tests/test_product.py -v -s --cov=. --cov-report term-missing


# # ---------------------------------------------------------------------------- Create product Tests ----------------------------------------------------------------------------


# def test_create_product(
#     client,
#     mock_create_product_data,
#     mock_vendor_token_data,
#     mock_vendor_data,
#     db,
#     approved_vendor_profile_inject,
#     roles_data_inject,
# ):
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)

#     assert register_vendor.status_code == 201

#     product = client.post(
#         "/products", json=mock_create_product_data, headers=mock_vendor_token_data
#     )

#     assert product.status_code == 201
#     assert product.json["success"] is True
#     assert product.json["message"] == "Product created successfully"
#     assert product.json["product"]["name"] == mock_create_product_data["name"]

#     tags = db.session.execute(db.select(models.ProductTag)).scalars().all()
#     sustainability_attributes = (
#         db.session.execute(db.select(models.SustainabilityAttribute)).scalars().all()
#     )

#     assert len(tags) == 2
#     assert len(sustainability_attributes) == 2


# def test_create_product_not_vendor(
#     client,
#     mock_create_product_data,
#     mock_token_data,
#     mock_user_data,
#     pending_vendor_profile_inject,
#     roles_data_inject,
# ):
#     register_user = client.post("/auth/register", json=mock_user_data)

#     assert register_user.status_code == 201

#     product = client.post(
#         "/products", json=mock_create_product_data, headers=mock_token_data
#     )

#     assert product.status_code == 403
#     assert product.json["success"] is False
#     assert product.json["message"] == "Vendor not approved"


# def test_create_product_name_validation_error(
#     client,
#     mock_create_product_data,
#     mock_vendor_token_data,
#     mock_vendor_data,
#     approved_vendor_profile_inject,
#     roles_data_inject,
# ):
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)

#     assert register_vendor.status_code == 201

#     mock_create_product_data["name"] = ""

#     product = client.post(
#         "/products", json=mock_create_product_data, headers=mock_vendor_token_data
#     )

#     assert product.status_code == 400
#     assert product.json["success"] is False
#     assert product.json["location"] == "view create product request validation"


# def test_create_product_description_validation_error(
#     client,
#     mock_create_product_data,
#     mock_vendor_token_data,
#     mock_vendor_data,
#     approved_vendor_profile_inject,
#     roles_data_inject,
# ):
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)

#     assert register_vendor.status_code == 201

#     mock_create_product_data["description"] = ""

#     product = client.post(
#         "/products", json=mock_create_product_data, headers=mock_vendor_token_data
#     )

#     assert product.status_code == 400
#     assert product.json["success"] is False
#     assert product.json["location"] == "view create product request validation"


# def test_create_product_price_validation_error(
#     client,
#     mock_create_product_data,
#     mock_vendor_token_data,
#     mock_vendor_data,
#     approved_vendor_profile_inject,
#     roles_data_inject,
# ):
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)

#     assert register_vendor.status_code == 201

#     mock_create_product_data["price"] = -1

#     product = client.post(
#         "/products", json=mock_create_product_data, headers=mock_vendor_token_data
#     )

#     assert product.status_code == 400
#     assert product.json["success"] is False
#     assert product.json["location"] == "view create product request validation"


# def test_create_product_tags_validation_error(
#     client,
#     mock_create_product_data,
#     mock_vendor_token_data,
#     mock_vendor_data,
#     approved_vendor_profile_inject,
#     roles_data_inject,
# ):
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)

#     assert register_vendor.status_code == 201

#     mock_create_product_data["tags"] = [i for i in ("a" * 15)]

#     product = client.post(
#         "/products", json=mock_create_product_data, headers=mock_vendor_token_data
#     )

#     assert product.status_code == 400
#     assert product.json["success"] is False
#     assert product.json["location"] == "view create product request validation"


# def test_create_product_sustainability_attributes_validation_error(
#     client,
#     mock_create_product_data,
#     mock_vendor_token_data,
#     mock_vendor_data,
#     approved_vendor_profile_inject,
#     roles_data_inject,
# ):
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)

#     assert register_vendor.status_code == 201

#     mock_create_product_data["sustainability_attributes"] = [i for i in ("a" * 10)]

#     product = client.post(
#         "/products", json=mock_create_product_data, headers=mock_vendor_token_data
#     )

#     assert product.status_code == 400
#     assert product.json["success"] is False
#     assert product.json["location"] == "view create product request validation"


# def test_create_product_stock_validation_error(
#     client,
#     mock_create_product_data,
#     mock_vendor_token_data,
#     mock_vendor_data,
#     approved_vendor_profile_inject,
#     roles_data_inject,
# ):
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)

#     assert register_vendor.status_code == 201

#     mock_create_product_data["stock_quantity"] = -1

#     product = client.post(
#         "/products", json=mock_create_product_data, headers=mock_vendor_token_data
#     )

#     assert product.status_code == 400
#     assert product.json["success"] is False
#     assert product.json["location"] == "view create product request validation"


# def test_create_product_order_quantity_validation_error(
#     client,
#     mock_create_product_data,
#     mock_vendor_token_data,
#     mock_vendor_data,
#     approved_vendor_profile_inject,
#     roles_data_inject,
# ):
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)

#     assert register_vendor.status_code == 201

#     mock_create_product_data["min_order_quantity"] = 0

#     product = client.post(
#         "/products", json=mock_create_product_data, headers=mock_vendor_token_data
#     )

#     assert product.status_code == 400
#     assert product.json["success"] is False
#     assert product.json["location"] == "view create product request validation"


# def test_create_product_Primary_Image_validation_error(
#     client,
#     mock_create_product_data,
#     mock_vendor_token_data,
#     mock_vendor_data,
#     approved_vendor_profile_inject,
#     roles_data_inject,
# ):
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)

#     assert register_vendor.status_code == 201

#     # invalid pattern
#     mock_create_product_data["primary_image_url"] = "a"

#     product = client.post(
#         "/products", json=mock_create_product_data, headers=mock_vendor_token_data
#     )

#     assert product.status_code == 400
#     assert product.json["success"] is False
#     assert product.json["location"] == "view create product request validation"

#     # too long
#     mock_create_product_data["primary_image_url"] = (
#         "https://example.com/image.jpg" + "a" * 600
#     )

#     product = client.post(
#         "/products", json=mock_create_product_data, headers=mock_vendor_token_data
#     )

#     assert product.status_code == 400
#     assert product.json["success"] is False
#     assert product.json["location"] == "view create product request validation"


# def test_create_product_Images_validation_error(
#     client,
#     mock_create_product_data,
#     mock_vendor_token_data,
#     mock_vendor_data,
#     approved_vendor_profile_inject,
#     roles_data_inject,
# ):
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)

#     assert register_vendor.status_code == 201

#     # no images
#     mock_create_product_data["images"] = None

#     product = client.post(
#         "/products", json=mock_create_product_data, headers=mock_vendor_token_data
#     )

#     assert product.status_code == 201
#     assert product.json["success"] is True

#     # more than 4 images
#     mock_create_product_data["images"] = [
#         "https://example.com/image.jpg",
#         "https://example.com/image.jpg",
#         "https://example.com/image.jpg",
#         "https://example.com/image.jpg",
#         "https://example.com/image.jpg",]

#     product = client.post(
#         "/products", json=mock_create_product_data, headers=mock_vendor_token_data
#     )

#     assert product.status_code == 400
#     assert product.json["success"] is False
#     assert product.json["location"] == "view create product request validation"

#     # invalid pattern
#     mock_create_product_data["images"] = ["a"]

#     product = client.post(
#         "/products", json=mock_create_product_data, headers=mock_vendor_token_data
#     )

#     assert product.status_code == 400
#     assert product.json["success"] is False
#     assert product.json["location"] == "view create product request validation"

#     # too long
#     mock_create_product_data["images"] = [("https://example.com/image.jpg" + "a" * 600)]

#     product = client.post(
#         "/products", json=mock_create_product_data, headers=mock_vendor_token_data
#     )

#     assert product.status_code == 400
#     assert product.json["success"] is False
#     assert product.json["location"] == "view create product request validation"


# # ---------------------------------------------------------------------------- Get product Tests ----------------------------------------------------------------------------


# def test_get_all_product(
#     client,
#     products_data_inject,
#     approved_vendor_profile_inject,
#     roles_data_inject,
#     users_data_inject,
# ):
#     product = client.get("/products")

#     assert product.status_code == 200
#     assert product.json["success"] is True
#     assert len(product.json["products"]) == 2


# def test_get_product_with_args(
#     client,
#     mock_multiple_create_product_data,
#     mock_vendor_token_data,
#     mock_vendor_data,
#     approved_vendor_profile_inject,
#     roles_data_inject,
# ):
#     # register vendor
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)

#     assert register_vendor.status_code == 201

#     # insert product
#     for product in mock_multiple_create_product_data:
#         product = client.post("/products", json=product, headers=mock_vendor_token_data)

#         assert product.status_code == 201

#     # get product
#     product = client.get(
#         "/products?min_price=10&page=1&per_page=20&max_price=30&tags=eco-friendly&tags=handmade&category_id=1"
#     )

#     assert product.status_code == 200
#     assert product.json["success"] is True
#     assert len(product.json["products"]) == 1
#     assert product.json["pagination"]["total"] == 1


# def test_get_product_invalid_args(client, roles_data_inject):
#     product = client.get("/products?min_price=-1")

#     assert product.status_code == 400
#     assert product.json["success"] is False
#     assert product.json["location"] == "view list products request validation"

#     product = client.get("/products?max_price=-1")

#     assert product.status_code == 400
#     assert product.json["success"] is False
#     assert product.json["location"] == "view list products request validation"


# # ---------------------------------------------------------------------------- Get product details Tests ----------------------------------------------------------------------------


# def test_get_product_details(client, products_data_inject, roles_data_inject):
#     product = client.get("/products/1")

#     assert product.status_code == 200
#     assert product.json["success"] is True
#     assert product.json["product"]["id"] == 1
#     assert len(product.json["product"]) == 15


# def test_get_product_details_repo_error(client, roles_data_inject):
#     product = client.get("/products/1")

#     assert product.status_code == 500
#     assert product.json["success"] is False
#     assert product.json["location"] == "view get product detail repo"


# # ---------------------------------------------------------------------------- Update product details Tests ----------------------------------------------------------------------------


# def test_update_product_details(
#     client,
#     mock_update_product_data,
#     mock_vendor_token_data,
#     mock_vendor_data,
#     db,
#     products_data_inject,
#     image_data_inject,
#     approved_vendor_profile_inject,
#     roles_data_inject,
# ):
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)

#     assert register_vendor.status_code == 201

#     product = client.put(
#         "/products/1", json=mock_update_product_data, headers=mock_vendor_token_data
#     )

#     assert product.status_code == 200
#     assert product.json["success"] is True
#     assert product.json["message"] == "Product updated successfully"
#     assert product.json["product"]["name"] == mock_update_product_data["name"]

#     tags = db.session.execute(db.select(models.ProductTag)).scalars().all()

#     sustainability_attributes = (
#         db.session.execute(db.select(models.SustainabilityAttribute)).scalars().all()
#     )

#     assert len(tags) == 2
#     assert len(sustainability_attributes) == 2


# def test_update_product_name_validation_error(
#     client,
#     mock_update_product_data,
#     mock_vendor_token_data,
#     mock_vendor_data,
#     approved_vendor_profile_inject,
#     roles_data_inject,
# ):
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)

#     assert register_vendor.status_code == 201

#     mock_update_product_data["name"] = ""

#     product = client.put(
#         "/products/1", json=mock_update_product_data, headers=mock_vendor_token_data
#     )

#     assert product.status_code == 400
#     assert product.json["success"] is False
#     assert product.json["location"] == "view update product request validation"


# def test_update_product_description_validation_error(
#     client,
#     mock_update_product_data,
#     mock_vendor_token_data,
#     mock_vendor_data,
#     approved_vendor_profile_inject,
#     roles_data_inject,
# ):
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)

#     assert register_vendor.status_code == 201

#     mock_update_product_data["description"] = ""

#     product = client.put(
#         "/products/1", json=mock_update_product_data, headers=mock_vendor_token_data
#     )

#     assert product.status_code == 400
#     assert product.json["success"] is False
#     assert product.json["location"] == "view update product request validation"


# def test_update_product_price_validation_error(
#     client,
#     mock_update_product_data,
#     mock_vendor_token_data,
#     mock_vendor_data,
#     approved_vendor_profile_inject,
#     roles_data_inject,
# ):
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)

#     assert register_vendor.status_code == 201

#     mock_update_product_data["price"] = -1

#     product = client.put(
#         "/products/1", json=mock_update_product_data, headers=mock_vendor_token_data
#     )

#     assert product.status_code == 400
#     assert product.json["success"] is False
#     assert product.json["location"] == "view update product request validation"


# def test_update_product_tags_validation_error(
#     client,
#     mock_update_product_data,
#     mock_vendor_token_data,
#     mock_vendor_data,
#     approved_vendor_profile_inject,
#     roles_data_inject,
# ):
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)

#     assert register_vendor.status_code == 201

#     mock_update_product_data["tags"] = [i for i in ("a" * 15)]

#     product = client.put(
#         "/products/1", json=mock_update_product_data, headers=mock_vendor_token_data
#     )

#     assert product.status_code == 400
#     assert product.json["success"] is False
#     assert product.json["location"] == "view update product request validation"


# def test_update_product_sustainability_attributes_validation_error(
#     client,
#     mock_update_product_data,
#     mock_vendor_token_data,
#     mock_vendor_data,
#     approved_vendor_profile_inject,
#     roles_data_inject,
# ):
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)

#     assert register_vendor.status_code == 201

#     mock_update_product_data["sustainability_attributes"] = [i for i in ("a" * 10)]

#     product = client.put(
#         "/products/1", json=mock_update_product_data, headers=mock_vendor_token_data
#     )

#     assert product.status_code == 400
#     assert product.json["success"] is False
#     assert product.json["location"] == "view update product request validation"


# def test_update_product_stock_validation_error(
#     client,
#     mock_update_product_data,
#     mock_vendor_token_data,
#     mock_vendor_data,
#     approved_vendor_profile_inject,
#     roles_data_inject,
# ):
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)

#     assert register_vendor.status_code == 201

#     mock_update_product_data["stock_quantity"] = -1

#     product = client.put(
#         "/products/1", json=mock_update_product_data, headers=mock_vendor_token_data
#     )

#     assert product.status_code == 400
#     assert product.json["success"] is False
#     assert product.json["location"] == "view update product request validation"


# def test_update_product_order_quantity_validation_error(
#     client,
#     mock_update_product_data,
#     mock_vendor_token_data,
#     mock_vendor_data,
#     approved_vendor_profile_inject,
#     roles_data_inject,
# ):
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)

#     assert register_vendor.status_code == 201

#     mock_update_product_data["min_order_quantity"] = 0

#     product = client.put(
#         "/products/1", json=mock_update_product_data, headers=mock_vendor_token_data
#     )

#     assert product.status_code == 400
#     assert product.json["success"] is False
#     assert product.json["location"] == "view update product request validation"


# def test_update_product_Primary_Image_validation_error(
#     client,
#     mock_update_product_data,
#     mock_vendor_token_data,
#     mock_vendor_data,
#     approved_vendor_profile_inject,
#     roles_data_inject,
# ):
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)

#     assert register_vendor.status_code == 201

#     # No input
#     mock_update_product_data["primary_image_url"] = None

#     product = client.put(
#         "/products/1", json=mock_update_product_data, headers=mock_vendor_token_data
#     )

#     assert product.status_code == 500
#     assert product.json["success"] is False
#     assert product.json["location"] == "view update product repo"

#     # invalid pattern
#     mock_update_product_data["primary_image_url"] = "a"

#     product = client.put(
#         "/products/1", json=mock_update_product_data, headers=mock_vendor_token_data
#     )

#     assert product.status_code == 400
#     assert product.json["success"] is False
#     assert product.json["location"] == "view update product request validation"

#     # too long
#     mock_update_product_data["primary_image_url"] = (
#         "https://example.com/image.jpg" + "a" * 600
#     )

#     product = client.put(
#         "/products/1", json=mock_update_product_data, headers=mock_vendor_token_data
#     )

#     assert product.status_code == 400
#     assert product.json["success"] is False
#     assert product.json["location"] == "view update product request validation"


# def test_update_product_Images_validation_error(
#     client,
#     mock_update_product_data,
#     mock_vendor_token_data,
#     mock_vendor_data,
#     approved_vendor_profile_inject,
#     roles_data_inject,
# ):
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)

#     assert register_vendor.status_code == 201

#     # No input
#     mock_update_product_data["images"] = None

#     product = client.put(
#         "/products/1", json=mock_update_product_data, headers=mock_vendor_token_data
#     )

#     assert product.status_code == 500
#     assert product.json["success"] is False
#     assert product.json["location"] == "view update product repo"

#     # more than 4 images
#     mock_update_product_data["images"] = [
#         "https://example.com/image.jpg",
#         "https://example.com/image.jpg",
#         "https://example.com/image.jpg",
#         "https://example.com/image.jpg",
#         "https://example.com/image.jpg",
#     ]

#     product = client.put(
#         "/products/1", json=mock_update_product_data, headers=mock_vendor_token_data
#     )

#     assert product.status_code == 400
#     assert product.json["success"] is False
#     assert product.json["location"] == "view update product request validation"

#     # invalid pattern
#     mock_update_product_data["images"] = ["a"]

#     product = client.put(
#         "/products/1", json=mock_update_product_data, headers=mock_vendor_token_data
#     )

#     assert product.status_code == 400
#     assert product.json["success"] is False
#     assert product.json["location"] == "view update product request validation"

#     # too long
#     mock_update_product_data["images"] = [
#         ("https://example.com/image.jpg" + "a" * 600)
#     ]

#     product = client.put(
#         "/products/1", json=mock_update_product_data, headers=mock_vendor_token_data
#     )

#     assert product.status_code == 400
#     assert product.json["success"] is False
#     assert product.json["location"] == "view update product request validation"


# def test_update_product_not_vendor(
#     client,
#     mock_update_product_data,
#     mock_vendor_token_data,
#     mock_vendor_data,
#     approved_vendor_profile_inject,
#     roles_data_inject,
# ):
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)

#     assert register_vendor.status_code == 201

#     product = client.put(
#         "/products/2", json=mock_update_product_data, headers=mock_vendor_token_data
#     )

#     assert product.status_code == 500
#     assert product.json["success"] is False
#     assert product.json["location"] == "view update product repo"


# # ----------------------------------------------------------------------------  Delete product test ----------------------------------------------------------------------------


# def test_delete_product(
#     client,
#     mock_vendor_token_data,
#     mock_vendor_data,
#     products_data_inject,
#     approved_vendor_profile_inject,
#     roles_data_inject,
# ):
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)

#     assert register_vendor.status_code == 201

#     product = client.delete("/products/1", headers=mock_vendor_token_data)

#     assert product.status_code == 200
#     assert product.json["success"] is True
#     assert product.json["message"] == "Product soft deleted (archived) successfully"
#     assert product.json["product"]["name"] == "Product 1"
#     assert product.json["product"]["is_active"] is False


# def test_delete_product_not_vendor(
#     client,
#     mock_vendor_token_data,
#     mock_vendor_data,
#     products_data_different_vendors_inject,
#     approved_vendor_profile_inject,
#     roles_data_inject,
# ):
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)

#     assert register_vendor.status_code == 201

#     product = client.delete("/products/2", headers=mock_vendor_token_data)

#     assert product.status_code == 403
#     assert product.json["success"] is False
#     assert product.json["message"] == "You are not authorized to delete this product"


# def test_delete_product_repo_error(
#     client,
#     mock_vendor_token_data,
#     mock_vendor_data,
#     approved_vendor_profile_inject,
#     roles_data_inject,
# ):
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)

#     assert register_vendor.status_code == 201

#     product = client.delete("/products/1", headers=mock_vendor_token_data)

#     assert product.status_code == 500
#     assert product.json["success"] is False
#     assert product.json["location"] == "view delete product repo"


# # ----------------------------------------------------------------------------  Get category test ----------------------------------------------------------------------------


# def test_get_category(client, category_data_inject, roles_data_inject):
#     category = client.get("/products/category")

#     assert category.status_code == 200
#     assert category.json["success"] is True


# def test_get_category_by_id(client, category_data_inject, roles_data_inject):
#     category = client.get("/products/category/1")

#     assert category.status_code == 200
#     assert category.json["success"] is True


# def test_get_category_by_id_invalid_id(client, category_data_inject, roles_data_inject):
#     category = client.get("/products/category/3")

#     assert category.status_code == 500
#     assert category.json["success"] is False
#     assert category.json["location"] == "view get category detail repo"


# # ----------------------------------------------------------------------------  Create wishlist test ----------------------------------------------------------------------------


# def test_create_wishlist(
#     client,
#     mock_vendor_token_data,
#     mock_vendor_data,
#     roles_data_inject,
#     products_data_inject,
# ):
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)

#     assert register_vendor.status_code == 201

#     wishlist = client.post("/products/wishlist/1", headers=mock_vendor_token_data)

#     assert wishlist.status_code == 200
#     assert wishlist.json["success"] is True


# def test_create_wishlist_product_already_in_wishlist(
#     client,
#     mock_vendor_token_data,
#     mock_vendor_data,
#     roles_data_inject,
#     products_data_inject,
# ):
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)

#     assert register_vendor.status_code == 201

#     wishlist = client.post("/products/wishlist/1", headers=mock_vendor_token_data)

#     assert wishlist.status_code == 200

#     # insert product to wishlist again
#     wishlist = client.post("/products/wishlist/1", headers=mock_vendor_token_data)

#     assert wishlist.status_code == 400
#     assert wishlist.json["success"] is False
#     assert wishlist.json["message"] == "Product already in wishlist"


# def test_create_wishlist_repo_error(
#     client,
#     mock_vendor_token_data,
#     mock_vendor_data,
#     roles_data_inject,
# ):
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)

#     assert register_vendor.status_code == 201

#     wishlist = client.post("/products/wishlist/1", headers=mock_vendor_token_data)

#     assert wishlist.status_code == 500
#     assert wishlist.json["success"] is False
#     assert wishlist.json["location"] == "view add product to wishlist repo"


# # ----------------------------------------------------------------------------  Delete wishlist test ----------------------------------------------------------------------------


# def test_delete_wishlist_product(
#     client,
#     mock_vendor_token_data,
#     mock_vendor_data,
#     roles_data_inject,
#     products_data_inject,
# ):
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)
#     assert register_vendor.status_code == 201

#     wishlist = client.post("/products/wishlist/1", headers=mock_vendor_token_data)
#     assert wishlist.status_code == 200

#     wishlist = client.delete("/products/wishlist/1", headers=mock_vendor_token_data)

#     assert wishlist.status_code == 200
#     assert wishlist.json["success"] is True
#     assert wishlist.json["message"] == "Product removed from wishlist successfully"


# def test_delete_wishlist_product_not_in_wishlist(
#     client,
#     mock_vendor_token_data,
#     mock_vendor_data,
#     roles_data_inject,
#     products_data_inject,
# ):
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)

#     assert register_vendor.status_code == 201

#     # make the wishlist
#     wishlist = client.post("/products/wishlist/1", headers=mock_vendor_token_data)

#     assert wishlist.status_code == 200

#     # delete product that is not in wishlist    
#     wishlist = client.delete("/products/wishlist/2", headers=mock_vendor_token_data)

#     assert wishlist.status_code == 404
#     assert wishlist.json["success"] is False
#     assert wishlist.json["message"] == "Product not in wishlist"


# def test_delete_wishlist_product_repo_error(
#     client,
#     mock_vendor_token_data,
#     mock_vendor_data,
#     roles_data_inject,
#     products_data_inject,
# ):
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)

#     assert register_vendor.status_code == 201

#     wishlist = client.delete("/products/wishlist/1", headers=mock_vendor_token_data)

#     assert wishlist.status_code == 500
#     assert wishlist.json["success"] is False
#     assert wishlist.json["location"] == "view remove product from wishlist repo"


# # ----------------------------------------------------------------------------  Get wishlist test ----------------------------------------------------------------------------


# def test_get_wishlist(
#     client,
#     mock_vendor_token_data,
#     mock_vendor_data,
#     roles_data_inject,
#     products_data_inject,
#     image_data_inject
# ):
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)

#     assert register_vendor.status_code == 201

#     wishlist_create = client.post("/products/wishlist/1", headers=mock_vendor_token_data)

#     assert wishlist_create.status_code == 200


#     wishlist = client.get("/products/wishlist", headers=mock_vendor_token_data)

#     wishlist_data = wishlist.json["wishlist"]

#     assert wishlist.status_code == 200
#     assert wishlist.json["success"] is True
#     assert wishlist.json["message"] == "Wishlist fetched successfully"
#     assert len(wishlist_data) == 2
#     assert wishlist_data["count"] == 1
#     assert len(wishlist_data["products"]) == 1
#     assert len(wishlist_data["products"][0]) == 5


# def test_get_wishlist_repo_error(
#     client,
#     mock_vendor_token_data,
#     mock_vendor_data,
#     roles_data_inject,
#     products_data_inject,
#     image_data_inject,
# ):
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)

#     assert register_vendor.status_code == 201

#     wishlist = client.get("/products/wishlist", headers=mock_vendor_token_data)

#     assert wishlist.status_code == 500
#     assert wishlist.json["success"] is False
#     assert wishlist.json["location"] == "view get wishlist repo"


# # ----------------------------------------------------------------------------  Get promotions test ----------------------------------------------------------------------------


# def test_get_promotions(client, mock_vendor_data, mock_vendor_token_data, promotions_data_inject, roles_data_inject):
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)

#     assert register_vendor.status_code == 201

#     promotions = client.get("/products/promotions", headers=mock_vendor_token_data)

#     assert promotions.status_code == 200
#     assert promotions.json["success"] is True
#     assert promotions.json["message"] == "Promotions fetched successfully"
#     assert len(promotions.json["promotions"]) == 1
#     assert len(promotions.json["promotions"][0]) == 12


# # ----------------------------------------------------------------------------  Get promotion detail test ----------------------------------------------------------------------------


# def test_get_promotion_detail(
#     client,
#     mock_vendor_data,
#     mock_vendor_token_data,
#     promotions_data_inject,
#     roles_data_inject,
# ):
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)

#     assert register_vendor.status_code == 201

#     promotion = client.get("/products/promotions/1", headers=mock_vendor_token_data)

#     assert promotion.status_code == 200
#     assert promotion.json["success"] is True
#     assert promotion.json["message"] == "Promotion fetched successfully"
#     assert len(promotion.json["promotion"]) == 16


# def test_get_promotion_detail_repo_error(
#     client,
#     mock_vendor_data,
#     mock_vendor_token_data,
#     roles_data_inject,
# ):
#     register_vendor = client.post("/auth/register", json=mock_vendor_data)

#     assert register_vendor.status_code == 201

#     promotion = client.get("/products/promotions/1", headers=mock_vendor_token_data)

#     assert promotion.status_code == 500
#     assert promotion.json["success"] is False
#     assert promotion.json["location"] == "view get promotion detail repo"


# ----------------------------------------------------------------------------  Get public vendor products test ----------------------------------------------------------------------------


def test_get_public_vendor_products(client, mock_vendor_data, mock_vendor_token_data, products_data_inject, roles_data_inject, category_data_inject, approved_vendor_profile_inject):
    register_vendor = client.post("/auth/register", json=mock_vendor_data)

    assert register_vendor.status_code == 201

    products = client.get(
        "/products/public-vendor-products?category_name=category1&business_name=Eco-Foods",
        headers=mock_vendor_token_data,
    )

    assert products.status_code == 200
    assert products.json["success"] is True
    assert products.json["products"] == "Public vendor products fetched successfully"
    assert len(products.json["products"]) == 1




# repo\product.py              102      8    92%   243-246 (done in vendor), 250-256 (done in order)

# router\product.py             51      0   100%

# schemas\product.py           278      3    99%   382, 387, 392 (done in vendor test)

# views\product.py             135     11    92%   80-82, 152-154, 419-420, 484-486 (exception errors)