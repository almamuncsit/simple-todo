"""Task routes module."""
from datetime import datetime
from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models.task import Task

bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')

@bp.route('/', methods=['GET'])
def get_tasks():
    """Get all tasks."""
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task."""
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict())

@bp.route('/', methods=['POST'])
def create_task():
    """Create a new task."""
    data = request.get_json()

    if not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400

    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        priority=data.get('priority', 'medium'),
        status=data.get('status', 'pending'),
        category_id=data.get('category_id')
    )

    if data.get('due_date'):
        try:
            task.due_date = datetime.fromisoformat(data['due_date'])
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400

    try:
        db.session.add(task)
        db.session.commit()
        return jsonify(task.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Invalid category ID'}), 400

@bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task."""
    task = Task.query.get_or_404(task_id)
    data = request.get_json()

    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'priority' in data:
        task.priority = data['priority']
    if 'status' in data:
        task.status = data['status']
    if 'category_id' in data:
        task.category_id = data['category_id']
    if 'due_date' in data:
        try:
            task.due_date = datetime.fromisoformat(data['due_date']) if data['due_date'] else None
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400

    try:
        db.session.commit()
        return jsonify(task.to_dict())
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Invalid category ID'}), 400

@bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task."""
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return '', 204
