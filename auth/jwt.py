from flask_jwt_extended import JWTManager

from repo.user import user_by_id_repo

jwt = JWTManager()

def init_jwt(app):
    jwt.init_app(app)

# Register a callback function that loads a user from your database whenever a protected route is accessed. 
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return user_by_id_repo(identity)
