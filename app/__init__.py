"""Flask application initialization module."""
from flask import Flask
from config import Config
from app.extensions import db
import app.models
from app.routes import task_routes, category_routes

def create_app():
    """Create and configure the Flask application."""
    flask_app = Flask(__name__)
    flask_app.config.from_object(Config)

    db.init_app(flask_app)

    flask_app.register_blueprint(task_routes.bp)
    flask_app.register_blueprint(category_routes.bp)

    return flask_app
