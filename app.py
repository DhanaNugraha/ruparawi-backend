# from middleware.before_request import auth_middleware
from config.settings import create_app
import os

os.environ.setdefault("FLASK_CONFIG", "config.local")

config_module = os.getenv("FLASK_CONFIG")

app = create_app(config_module)

# auth_middleware(app)  # Register middleware


