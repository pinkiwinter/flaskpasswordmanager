from flask import Flask
from flask_migrate import Migrate
from .config import Config
from dotenv import load_dotenv
from .models import db
from .routes import jwt, register_routes

def create_app():
    app = Flask(__name__)
    migrate = Migrate(app, db)
    app.config.from_object(Config)

    load_dotenv()

    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    register_routes(app)

    return app

