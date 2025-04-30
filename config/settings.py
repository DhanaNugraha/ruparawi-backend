from flask import Flask, request
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
    ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3002",
        "https://ruparawi-frontend.vercel.app",
    ]

    @app.after_request
    def add_cors_headers(response):
        origin = request.headers.get("Origin", '')

        if origin in ALLOWED_ORIGINS:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"

        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, PUT, DELETE"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        
        return response

