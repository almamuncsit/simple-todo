"""Flask application initialization module."""

from flask import Flask
from config import Config
from app.extensions import db
from app.routes import task_routes, category_routes

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(task_routes.bp)
    app.register_blueprint(category_routes.bp)

    return app
