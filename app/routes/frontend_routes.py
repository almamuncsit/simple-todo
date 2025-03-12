"""Frontend routes module."""
from flask import Blueprint, render_template

bp = Blueprint('frontend', __name__)

@bp.route('/')
def home():
    """Render home page."""
    return render_template('home.html')

@bp.route('/categories')
def categories():
    """Render categories page."""
    return render_template('categories.html')

@bp.route('/tasks')
def tasks():
    """Render tasks page."""
    return render_template('tasks.html')
