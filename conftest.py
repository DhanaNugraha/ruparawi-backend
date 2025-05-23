from datetime import timedelta
import pytest
from config.settings import cors_setup, create_app
from instance.database import db as _db
import models
from shared.time import datetime_from_string, now
import os


@pytest.fixture
def test_app():
    config_module = os.environ["FLASK_CONFIG"] = "config.testing"
    app = create_app(config_module)
    cors_setup(app)
    with app.app_context():
        _db.create_all()
        _db.session.rollback()

    yield app

    with app.app_context():
        _db.session.rollback()
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def db(test_app):
    with test_app.app_context():
        yield _db


@pytest.fixture
def client(test_app):
    with test_app.test_client() as client:
        yield client
    # print("Tearing down the test client")


@pytest.fixture
def users_data_inject(test_app):
    users_data = [
        {
            "id": 1,
            "username": "john",
            "email": "john.doe@example.com",
            "password_hash": "testing/password",
            "created_at": datetime_from_string(str(now())),
            "updated_at": datetime_from_string(str(now())),
        },
        {
            "id": 2,
            "username": "jane",
            "email": "jane.smith@example.com",
            "password_hash": "testing/password",
            "created_at": datetime_from_string(str(now())),
            "updated_at": datetime_from_string(str(now())),
        },
    ]
    with test_app.app_context():
        users_list = []
        for user in users_data:
            user_model = models.User(**user)
            users_list.append(user_model)

        _db.session.add_all(users_list)
        _db.session.commit()

        return users_list


@pytest.fixture
def roles_data_inject(test_app):
    roles_data = [
        {
            "id": 1,
            "name": "buyer",
        },
        {
            "id": 2,
            "name": "vendor",
        },
        {
            "id": 3,
            "name": "admin",
        },
    ]
    with test_app.app_context():
        roles_list = []
        for roles in roles_data:
            roles_model = models.UserRole(**roles)
            roles_list.append(roles_model)

        _db.session.add_all(roles_list)
        _db.session.commit()

        return roles_list


@pytest.fixture
def products_data_inject(test_app):
    products_data = [
        {
            "id": 1,
            "name": "Product 1",
            "description": "Description 1",
            "price": 10.99,
            "category_id": 1,
            "vendor_id": 1,
            "stock_quantity": 10,
            "min_order_quantity": 1,
            "average_rating": 4.5,
            "review_count": 5,
            "is_active": True,
            "created_at": datetime_from_string(str(now())),
            "updated_at": datetime_from_string(str(now())),
        },
        {
            "id": 2,
            "name": "Product 2",
            "description": "Description 2",
            "price": 19.99,
            "category_id": 2,
            "vendor_id": 1,
            "stock_quantity": 5,
            "min_order_quantity": 1,
            "average_rating": 4.0,
            "review_count": 3,
            "is_active": True,
            "created_at": datetime_from_string(str(now())),
            "updated_at": datetime_from_string(str(now())),
        },
    ]
    with test_app.app_context():
        products_list = []
        for product in products_data:
            product_model = models.Product(**product)
            products_list.append(product_model)

        _db.session.add_all(products_list)
        _db.session.commit()

        return products_list


@pytest.fixture
def products_data_different_vendors_inject(test_app):
    products_data = [
        {
            "id": 1,
            "name": "Product 1",
            "description": "Description 1",
            "price": 10.99,
            "category_id": 1,
            "vendor_id": 1,
            "stock_quantity": 10,
            "min_order_quantity": 1,
            "average_rating": 4.5,
            "review_count": 5,
            "is_active": True,
            "created_at": datetime_from_string(str(now())),
            "updated_at": datetime_from_string(str(now())),
        },
        {
            "id": 2,
            "name": "Product 2",
            "description": "Description 2",
            "price": 19.99,
            "category_id": 2,
            "vendor_id": 2,
            "stock_quantity": 5,
            "min_order_quantity": 1,
            "average_rating": 4.0,
            "review_count": 3,
            "is_active": True,
            "created_at": datetime_from_string(str(now())),
            "updated_at": datetime_from_string(str(now())),
        },
    ]
    with test_app.app_context():
        products_list = []
        for product in products_data:
            product_model = models.Product(**product)
            products_list.append(product_model)

        _db.session.add_all(products_list)
        _db.session.commit()

        return products_list


@pytest.fixture
def admins_data_inject(test_app):
    admins_data = [
        {
            "user_id": 1,
            "access_level": "admin",
        },
    ]
    with test_app.app_context():
        admins_list = []
        for admin in admins_data:
            admin_model = models.AdminUser(**admin)
            admins_list.append(admin_model)

        _db.session.add_all(admins_list)
        _db.session.commit()

        return admins_list


@pytest.fixture
def category_data_inject(test_app):
    category_data = [
        {
            "id": 1,
            "name": "category1",
            "description": "test category description",
        },
        {
            "id": 2,
            "name": "category2",
            "description": "test category description",
            "parent_category_id": 1,
        },
    ]
    with test_app.app_context():
        category_list = []
        for category in category_data:
            category_model = models.ProductCategory(**category)
            category_list.append(category_model)

        _db.session.add_all(category_list)
        _db.session.commit()

        return category_list


@pytest.fixture
def approved_vendor_profile_inject(test_app):
    vendor_profile_data = [
        {
            "user_id": 1,
            "vendor_status": "approved",
            "business_name": "Eco Foods",
            "business_email": "vendor@ecofoods.com",
            "business_phone": "+1234567890",
            "business_address": "123 Green St, Eco City",
            "business_description": "Organic food supplier",
            "business_logo_url": "https://example.com/profile.jpg",
        },
        {
            "user_id": 2,
            "vendor_status": "approved",
            "business_name": "Eco Foods",
            "business_email": "vendor@ecofoods.com",
            "business_phone": "+1234567890",
            "business_address": "123 Green St, Eco City",
            "business_description": "Organic food supplier",
            "business_logo_url": "https://example.com/profile.jpg",
        },
    ]
    with test_app.app_context():
        vendor_profile_list = []
        for vendor_profile in vendor_profile_data:
            vendor_profile_model = models.VendorProfile(**vendor_profile)
            vendor_profile_list.append(vendor_profile_model)

        _db.session.add_all(vendor_profile_list)
        _db.session.commit()

        return vendor_profile_list


@pytest.fixture
def pending_vendor_profile_inject(test_app):
    vendor_profile_data = [
        {
            "user_id": 1,
            "vendor_status": "pending",
            "business_name": "Eco Foods",
            "business_email": "vendor@ecofoods.com",
            "business_phone": "+1234567890",
            "business_address": "123 Green St, Eco City",
            "business_description": "Organic food supplier",
            "business_logo_url": "https://example.com/profile.jpg",
        },
    ]
    with test_app.app_context():
        vendor_profile_list = []
        for vendor_profile in vendor_profile_data:
            vendor_profile_model = models.VendorProfile(**vendor_profile)
            vendor_profile_list.append(vendor_profile_model)

        _db.session.add_all(vendor_profile_list)
        _db.session.commit()

        return vendor_profile_list


@pytest.fixture
def cart_data_inject(test_app):
    cart_data = [
        {
            "id": 1,
            "user_id": 1,
        },
    ]
    with test_app.app_context():
        cart_list = []
        for cart in cart_data:
            cart_model = models.ShoppingCart(**cart)
            cart_list.append(cart_model)

        _db.session.add_all(cart_list)
        _db.session.commit()

        return cart_list


@pytest.fixture
def cart_item_data_inject(test_app):
    cart_item_data = [
        {
            "id": 1,
            "cart_id": 1,
            "product_id": 1,
            "quantity": 2,
        },
    ]
    with test_app.app_context():
        cart_item_list = []
        for cart_item in cart_item_data:
            cart_item_model = models.CartItem(**cart_item)
            cart_item_list.append(cart_item_model)

        _db.session.add_all(cart_item_list)
        _db.session.commit()

        return cart_item_list


@pytest.fixture
def address_data_inject(test_app):
    address_data = [
        {
            "id": 1,
            "user_id": 1,
            "address_line1": "123 Main St",
            "address_line2": "123 Main St",
            "city": "New York",
            "state": "NY",
            "postal_code": "10001",
            "country": "USA",
            "is_default": True,
        }
    ]
    with test_app.app_context():
        address_list = []
        for address in address_data:
            address_model = models.UserAddress(**address)
            address_list.append(address_model)

        _db.session.add_all(address_list)
        _db.session.commit()

        return address_list


@pytest.fixture
def payment_method_data_inject(test_app):
    payment_method_data = [
        {
            "id": 1,
            "user_id": 1,
            "payment_type": "credit_card",
            "provider": "Visa",
            "account_number": "4111111111111111",
            "is_default": True,
        }
    ]
    with test_app.app_context():
        payment_method_list = []
        for payment_method in payment_method_data:
            payment_method_model = models.UserPaymentMethod(**payment_method)
            payment_method_list.append(payment_method_model)

        _db.session.add_all(payment_method_list)
        _db.session.commit()

        return payment_method_list


@pytest.fixture
def order_data_inject(test_app):
    order_data = [
        {
            "id": 1,
            "user_id": 1,
            "total_amount": 100.00,
            "shipping_address_id": 1,
            "billing_address_id": 1,
            "payment_method_id": 1,
            "payment_status": "pending",
            "tracking_number": "1234567890",
            "notes": "Order notes",
            "created_at": datetime_from_string(str(now())),
            "order_number": "1234567890",
        }
    ]
    with test_app.app_context():
        order_list = []
        for order in order_data:
            order_model = models.Order(**order)
            order_list.append(order_model)

        _db.session.add_all(order_list)
        _db.session.commit()

        return order_list


@pytest.fixture
def order_item_data_inject(test_app):
    order_item_data = [
        {
            "id": 1,
            "order_id": 1,
            "product_id": 1,
            "quantity": 2,
            "unit_price": 10.00,
            "total_price": 20.00,
            "vendor_id": 1,
        },
        {
            "id": 2,
            "order_id": 1,
            "product_id": 2,
            "quantity": 1,
            "unit_price": 10.00,
            "total_price": 10.00,
            "vendor_id": 1,
        },
    ]
    with test_app.app_context():
        order_item_list = []
        for order_item in order_item_data:
            order_item_model = models.OrderItem(**order_item)
            order_item_list.append(order_item_model)

        _db.session.add_all(order_item_list)
        _db.session.commit()

        return order_item_list


@pytest.fixture
def promotions_data_inject(test_app):
    promotions_data = [
        {
            "id": 1,
            "title": "Test Promotion",
            "description": "This is a test promotion",
            "promo_code": "TESTPROMO",
            "discount_value": 10.00,
            "promotion_type": "percentage_discount",
            "start_date": datetime_from_string(str(now() - timedelta(days=7))),
            "end_date": datetime_from_string(str(now() + timedelta(days=6))),
            "admin_id": 1,
            "image_url": None,
            "max_discount": None,
            "usage_limit": 1,
        },
        {
            "id": 2,
            "title": "Test Promotion",
            "description": "This is a test promotion",
            "promo_code": "TESTPROMO2",
            "discount_value": 10.00,
            "promotion_type": "percentage_discount",
            "start_date": datetime_from_string(str(now() - timedelta(days=7))),
            "end_date": datetime_from_string(str(now() - timedelta(days=6))),
            "admin_id": 1,
            "image_url": None,
            "max_discount": None,
            "usage_limit": 1,
        },
    ]
    with test_app.app_context():
        promotions_list = []
        for promotions in promotions_data:
            promotions_model = models.Promotion(**promotions)
            promotions_list.append(promotions_model)

        _db.session.add_all(promotions_list)
        _db.session.commit()

        return promotions_list


@pytest.fixture
def article_data_inject(test_app):
    article_data = [
        {
            "id": 1,
            "title": "article test",
            "content": "test content ......................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................",
            "author_id": 1,
        }
    ]
    with test_app.app_context():
        article_list = []
        for article in article_data:
            article_model = models.Article(**article)
            article_list.append(article_model)

        _db.session.add_all(article_list)
        _db.session.commit()

        return article_list


@pytest.fixture
def image_data_inject(test_app):
    image_data = [
        {
            "id": 1,
            "product_id": 1,
            "image_url": "https://example.com/image1.jpg",
            "is_primary": True,
        },
        {
            "id": 2,
            "product_id": 1,
            "image_url": "https://example.com/image2.jpg",
            "is_primary": False,
        },
    ]
    with test_app.app_context():
        image_list = []
        for image in image_data:
            image_model = models.ProductImage(**image)
            image_list.append(image_model)

        _db.session.add_all(image_list)
        _db.session.commit()

        return image_list


@pytest.fixture
def product_review_data_inject(test_app):
    product_review_data = [
        {"id": 1, "product_id": 1, "user_id": 1, "rating": 5, "comment": "test inject"},
    ]
    with test_app.app_context():
        product_review_list = []
        for product_review in product_review_data:
            product_review_model = models.ProductReview(**product_review)
            product_review_list.append(product_review_model)

        _db.session.add_all(product_review_list)
        _db.session.commit()

        return product_review_list


@pytest.fixture
def testimonial_data_inject(test_app):
    testimonial_data = [
        {"id": 1, "message": "test", "vendor_id": 1},
    ]
    with test_app.app_context():
        testimonial_list = []
        for testimonial in testimonial_data:
            testimonial_model = models.VendorTestimonial(**testimonial)
            testimonial_list.append(testimonial_model)

        _db.session.add_all(testimonial_list)
        _db.session.commit()

        return testimonial_list


@pytest.fixture
def mock_user_data():
    return {
        "username": "eco_buyer",
        "email": "buyer@example.com",
        "password": "sustainable123",
    }


@pytest.fixture
def mock_login_data():
    return {
        "email": "buyer@example.com",
        "password": "sustainable123",
    }


@pytest.fixture
def mock_token_data():
    return {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NDgxMjcxNSwianRpIjoiYTg1NDlkZjctYjJlNS00MWVkLWJlNzktMWY0NmNjMzZiNDk4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NDQ4MTI3MTUsImNzcmYiOiJiOWNkN2E4NC04YjUyLTQ5ZWEtYjY2ZC1jNTU3ZDQ1MzUzYzEiLCJ1c2VybmFtZSI6ImVjb19idXllciIsImVtYWlsIjoiYnV5ZXJAZXhhbXBsZS5jb20iLCJpc192ZW5kb3IiOmZhbHNlLCJpc19hZG1pbiI6ZmFsc2V9.4c1EcKMgb__oQLqBjptFxjl9_up9hbPXzNuguQZRGQQ"
    }


@pytest.fixture
def mock_refresh_token_data():
    return {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NjI2NDA1NCwianRpIjoiZDAwZjVjZDgtNmEyMy00ZGFlLWI2ZTYtYjViYjczNmQwN2I1IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiIxIiwibmJmIjoxNzQ2MjY0MDU0LCJjc3JmIjoiMDMzM2ZiMzgtOTkxNy00MWQzLTg3YzEtYTIzYjAxNjhiN2UxIiwiZXhwIjoxNzQ4ODU2MDU0LCJ1c2VybmFtZSI6ImVjb19idXllciIsImVtYWlsIjoiYnV5ZXJAZXhhbXBsZS5jb20ifQ.DRtVTPOH9Vw2H1RCTZJb7zPMJT3O5JJ_xjr2UOEKPD0"
    }


@pytest.fixture
def mock_update_user_data():
    return {
        "bio": "test update bio",
        "first_name": "test update first name",
        "last_name": "test update last name",
        "profile_image_url": "https://example.com/profile.jpg",
        "password": "updated123",
    }


@pytest.fixture
def mock_vendor_data():
    return {
        "username": "eco_seller",
        "email": "seller@example.com",
        "password": "sustainable123",
    }


@pytest.fixture
def mock_vendor_token_data():
    return {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NDkwMzY4MCwianRpIjoiODczZjM4OTMtMWRjYy00YTRmLThlNTYtYWEzYWFhNTA4N2M1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NDQ5MDM2ODAsImNzcmYiOiJhMzU4YTczOS1lOTA3LTQ4YzItOTI3YS00ZGM4MmRmNjhkMjIiLCJ1c2VybmFtZSI6ImVjb19zZWxsZXIiLCJlbWFpbCI6InNlbGxlckBleGFtcGxlLmNvbSIsImlzX3ZlbmRvciI6dHJ1ZSwiaXNfYWRtaW4iOmZhbHNlfQ.wxF4C495DnFjDn3Vq4K7g1VSnCT9Xci8BblYi7ALIkY"
    }


@pytest.fixture
def mock_create_product_data():
    return {
        "name": "testproduct",
        "description": "test product description",
        "price": 25.99,
        "tags": ["eco-friendly", "handmade"],
        "sustainability_attributes": ["organic", "carbon-neutral"],
        "stock_quantity": 100,
        "min_order_quantity": 2,
        "primary_image_url": "https://example.com/image.jpg",
        "images": ["https://example.com/image2.jpg"],
    }


@pytest.fixture
def mock_multiple_create_product_data():
    return [
        {
            "name": "testproduct 1",
            "description": "test product description 1",
            "price": 25.99,
            "tags": ["eco-friendly", "handmade"],
            "sustainability_attributes": ["organic", "carbon-neutral"],
            "stock_quantity": 100,
            "min_order_quantity": 2,
            "category_id": 1,
            "primary_image_url": "https://example.com/image.jpg",
        },
        {
            "name": "testproduct 2",
            "description": "test product description 2",
            "price": 15.99,
            "tags": ["eco-friendly", "cheap"],
            "sustainability_attributes": ["organic", "carbon-neutral"],
            "stock_quantity": 100,
            "min_order_quantity": 2,
            "primary_image_url": "https://example.com/image.jpg",
        },
    ]


@pytest.fixture
def mock_update_product_data():
    return {
        "name": "updated product",
        "description": "test product description",
        "price": 25.99,
        "category_id": 1,
        "tags": ["eco-friendly", "handmade"],
        "sustainability_attributes": ["organic", "carbon-neutral"],
        "stock_quantity": 100,
        "min_order_quantity": 2,
        "is_active": True,
        "primary_image_url": "https://example.com/image.jpg",
        "images": ["https://example.com/image2.jpg"],
    }


@pytest.fixture
def mock_category_data():
    return {
        "name": "category",
        "description": "test category description",
    }


@pytest.fixture
def mock_subcategory_data():
    return {
        "name": "subcategory",
        "description": "test subcategory description",
        "parent_category_id": 2,
    }


@pytest.fixture
def mock_update_category_data():
    return {
        "name": "category updated",
        "description": "test category description updated",
        "parent_category_id": 1,
    }


@pytest.fixture
def mock_vendor_apply_data():
    return {
        "business_name": "Eco Foods",
        "business_email": "vendor@ecofoods.com",
        "business_phone": "+1234567890",
        "business_address": "123 Green St, Eco City",
        "business_description": "Organic food supplier",
        "business_logo_url": "https://example.com/profile.jpg",
    }


@pytest.fixture
def mock_vendor_update_data():
    return {
        "business_name": "Eco Foods updated",
        "business_email": "vendorupdated@ecofoods.com",
        "business_phone": "+1234567890",
        "business_address": "123 Green St, Eco City",
        "business_description": "Organic food supplier",
        "business_logo_url": "https://example.com/profile.jpg",
    }


@pytest.fixture
def mock_admin_vendor_review_data():
    return {"action": "approve", "reason": "testing"}


@pytest.fixture
def mock_add_cart_item():
    return {"product_id": 1, "quantity": 1}


@pytest.fixture
def mock_update_cart_item():
    return {"product_id": 1, "quantity": 5}


@pytest.fixture
def mock_create_address_data():
    return {
        "address_line1": "123 Main St",
        "address_line2": "123 Main St",
        "city": "New York",
        "state": "NY",
        "postal_code": "10001",
        "country": "USA",
        "is_default": True,
    }


@pytest.fixture
def mock_update_address_data():
    return {
        "address_line1": "123 Main St",
        "address_line2": "123 Main St",
        "city": "New York",
        "state": "NY",
        "postal_code": "10001",
        "country": "USA",
        "is_default": True,
    }


@pytest.fixture
def mock_create_payment_method_data():
    return {
        "payment_type": "credit card",
        "provider": "Visa",
        "account_number": "4111111111111111",
        "expiry_date": "12/25",
        "is_default": True,
    }


@pytest.fixture
def mock_update_payment_method_data():
    return {
        "payment_type": "credit card",
        "provider": "Visa",
        "account_number": "4111111111111111",
        "expiry_date": "12/40",
        "is_default": True,
    }


@pytest.fixture
def mock_promotion_data():
    return {
        "title": "Test Promotion",
        "description": "This is a test promotion",
        "promo_code": "TESTPROMO",
        "discount_value": 10.00,
        "promotion_type": "percentage_discount",
        "start_date": "2000-12-31",
        "end_date": "2100-12-31",
        "usage_limit": 1,
        "product_ids": [1, 2],
        "category_names": ["category1", "category2"],
        "image_url": "https://example.com/promotion.jpg",
    }


@pytest.fixture
def mock_article_data():
    return {
        "title": "article test",
        "content": "test content ......................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................",
    }


@pytest.fixture
def mock_product_review_data():
    return {"product_id": 1, "user_id": 1, "rating": 5, "comment": "test"}


@pytest.fixture
def mock_pre_checkout_data():
    return {
        "promotion_code": "TESTPROMO",
    }


@pytest.fixture
def mock_checkout_data():
    return {
        "shipping_address_id": 1,
        "billing_address_id": 1,
        "payment_method_id": 1,
        "notes": "test notes",
        "promotion_code": "TESTPROMO",
    }


@pytest.fixture
def mock_update_order_data():
    return {
        "status": "shipped",
        "notes": "test notes",
    }


@pytest.fixture
def mock_testimonial_data():
    return {"vendor_id": 1, "message": "test message testimonial"}
