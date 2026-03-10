from flask import Blueprint, request, jsonify
from app import db  
from models import Category
from flask_jwt_extended import jwt_required, get_jwt_identity

category_bp = Blueprint('categories', __name__, url_prefix='/api/categories')

@category_bp.route('/', methods=['GET'])
def get_categories():
    try:
        categories = Category.query.all()
        return jsonify([c.to_dict() for c in categories]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@category_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    try:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        
        return jsonify(category.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@category_bp.route('/', methods=['POST'])
@jwt_required()
def create_category():
    try:
        data = request.get_json()
        
        if 'name' not in data or not data['name']:
            return jsonify({'error': 'Category name is required'}), 400
        
        existing = Category.query.filter_by(name=data['name']).first()
        if existing:
            return jsonify({'error': 'Category already exists'}), 409
        
        new_category = Category(
            name=data['name'],
            description=data.get('description', '')
        )
        
        db.session.add(new_category)
        db.session.commit()
        
        return jsonify(new_category.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500