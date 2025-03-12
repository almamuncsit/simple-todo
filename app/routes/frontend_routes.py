"""Frontend routes module."""
from flask import Blueprint, render_template
from app.models.category import Category
from app.models.task import Task

bp = Blueprint('frontend', __name__)

@bp.route('/')
def home():
    """Render home page."""
    return render_template('home.html')

@bp.route('/categories')
def categories():
    """Render categories page."""
    all_categories = Category.query.all()
    return render_template('categories.html', categories=all_categories)

@bp.route('/tasks')
def tasks():
    """Render tasks page."""
    all_tasks = Task.query.all()
    return render_template('tasks.html', tasks=all_tasks)