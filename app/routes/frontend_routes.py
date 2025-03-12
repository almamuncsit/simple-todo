"""Frontend routes module."""
from flask import Blueprint, render_template, current_app
import requests

bp = Blueprint('frontend', __name__)

def get_api_url(endpoint):
    """Get full API URL."""
    server_name = current_app.config.get('SERVER_NAME', 'localhost:5000')
    return f"http://{server_name}/api{endpoint}"

@bp.route('/')
def home():
    """Render home page."""
    return render_template('home.html')

@bp.route('/categories')
def categories():
    """Render categories page."""
    response = requests.get(get_api_url('/categories/'))
    categories_data = response.json() if response.ok else []
    return render_template('categories.html', categories=categories_data)

@bp.route('/tasks')
def tasks():
    """Render tasks page."""
    response = requests.get(get_api_url('/tasks/'))
    tasks_data = response.json() if response.ok else []
    return render_template('tasks.html', tasks=tasks_data)
