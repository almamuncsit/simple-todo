# Add docstring for the module
"""Flask application initialization module."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes import task_routes, category_routes
    app.register_blueprint(task_routes.bp)
    app.register_blueprint(category_routes.bp)

    return app