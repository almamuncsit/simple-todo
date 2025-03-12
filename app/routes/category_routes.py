"""Category routes module."""
from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models.category import Category

bp = Blueprint('categories', __name__, url_prefix='/api/categories')

@bp.route('/', methods=['GET'])
def get_categories():
    """Get all categories."""
    categories = Category.query.all()
    return jsonify([category.to_dict() for category in categories])

@bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """Get a specific category."""
    category = Category.query.get_or_404(category_id)
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
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Category name must be unique'}), 400

@bp.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    """Update a category."""
    category = Category.query.get_or_404(category_id)
    data = request.get_json()
    
    if 'name' in data:
        category.name = data['name']
    if 'description' in data:
        category.description = data['description']
    
    try:
        db.session.commit()
        return jsonify(category.to_dict())
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Category name must be unique'}), 400

@bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    """Delete a category."""
    category = Category.query.get_or_404(category_id)
    
    try:
        db.session.delete(category)
        db.session.commit()
        return '', 204
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Cannot delete category with associated tasks'}), 400
