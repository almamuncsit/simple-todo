"""Category routes module."""
from flask import Blueprint, request, jsonify
from app import db
from app.models.category import Category

bp = Blueprint('categories', __name__, url_prefix='/api/categories')

@bp.route('/', methods=['GET'])
def get_categories():
    """Get all categories."""
    categories = Category.query.all()
    return jsonify([category.to_dict() for category in categories])

@bp.route('/<int:id>', methods=['GET'])
def get_category(id):
    """Get a specific category."""
    category = Category.query.get_or_404(id)
    return jsonify(category.to_dict())

@bp.route('/', methods=['POST'])
def create_category():
    """Create a new category."""
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
    
    category = Category(
        name=data['name'],
        description=data.get('description', '')
    )
    
    try:
        db.session.add(category)
        db.session.commit()
        return jsonify(category.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Category name must be unique'}), 400

@bp.route('/<int:id>', methods=['PUT'])
def update_category(id):
    """Update a category."""
    category = Category.query.get_or_404(id)
    data = request.get_json()
    
    if 'name' in data:
        category.name = data['name']
    if 'description' in data:
        category.description = data['description']
    
    try:
        db.session.commit()
        return jsonify(category.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Category name must be unique'}), 400

@bp.route('/<int:id>', methods=['DELETE'])
def delete_category(id):
    """Delete a category."""
    category = Category.query.get_or_404(id)
    
    try:
        db.session.delete(category)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Cannot delete category with associated tasks'}), 400
