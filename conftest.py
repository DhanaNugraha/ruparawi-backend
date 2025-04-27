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
            "is_vendor": False,
        },
        {
            "id": 2,
            "username": "jane",
            "email": "jane.smith@example.com",
            "password_hash": "testing/password",
            "created_at": datetime_from_string(str(now())),
            "updated_at": datetime_from_string(str(now())),
            "is_vendor": False,
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
            "name": "updated product",
            "description": "test product description",
        },
        {
            "id": 2,
            "name": "updated product",
            "description": "test product description",
            "parent_category_id": 1
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
def mock_update_user_data():
    return {
        "bio": "test update bio",
        "first_name": "test update first name",
        "last_name": "test update last name",
        "profile_image_url": "https://example.com/profile.jpg"
    }

@pytest.fixture
def mock_vendor_data():
    return {
        "username": "eco_seller",
        "email": "seller@example.com",
        "password": "sustainable123",
        "is_vendor": True
    }


@pytest.fixture
def mock_vendor_login_data():
    return {
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
            "category_id": 1
        },
        {
            "name": "testproduct 2",
            "description": "test product description 2",
            "price": 15.99,
            "tags": ["eco-friendly", "cheap"],
            "sustainability_attributes": ["organic", "carbon-neutral"],
            "stock_quantity": 100,
            "min_order_quantity": 2,
        }
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
        "is_active": True
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
        "parent_category_id": 2
    }


@pytest.fixture
def mock_update_category_data():
    return {
        "name": "category updated",
        "description": "test category description updated",
        "parent_category_id": 1
    }