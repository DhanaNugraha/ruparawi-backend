from flask import Flask
from instance.database import init_db
from auth.jwt import init_jwt
import models
import router
from config import configure_app


def create_app(config_module = "config.local"):
    app = Flask(__name__)
    app.config.from_object(config_module)
    init_db(app)
    init_jwt(app)
    configure_app()
    app.register_blueprint(router.auth_router)
    app.register_blueprint(router.user_router)
    app.register_blueprint(router.products_router)
    app.register_blueprint(router.admin_router)
    app.register_blueprint(router.vendor_router)
    app.register_blueprint(router.order_router)
    return app


def cors_setup(app):
    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, PUT, DELETE"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response
