from .auth import authb
from .passwords import add_accounts, accounts
from flask_jwt_extended import JWTManager

jwt = JWTManager()

def register_routes(app):
    app.register_blueprint(authb)
    app.register_blueprint(accounts)
    app.register_blueprint(add_accounts)
