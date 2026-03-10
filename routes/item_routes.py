# routes/item_routes.py
from flask import Blueprint, request, jsonify
from extensions import db
from models import Item, Category, User, Request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_

item_bp = Blueprint('items', __name__, url_prefix='/api/items')

# ========== PUBLIC ROUTES (No authentication required) ==========

@item_bp.route('/', methods=['GET'])
def get_items():
    """
    Get all available items with optional filtering
    Query parameters:
    - category: filter by category ID
    - location: filter by pickup location
    - search: search in title and description
    - available: only show available items (default true)
    """
    try:
        # Start with query for available items
        query = Item.query.filter_by(is_available=True)
        
        # Filter by category
        category_id = request.args.get('category')
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        # Filter by location (case-insensitive partial match)
        location = request.args.get('location')
        if location:
            query = query.filter(Item.pickup_location.ilike(f'%{location}%'))
        
        # Search in title and description
        search = request.args.get('search')
        if search:
            query = query.filter(
                or_(
                    Item.title.ilike(f'%{search}%'),
                    Item.description.ilike(f'%{search}%')
                )
            )
        
        # Order by newest first
        items = query.order_by(Item.created_at.desc()).all()
        
        return jsonify([item.to_dict() for item in items]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@item_bp.route('/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """
    Get single item by ID
    """
    try:
        item = Item.query.get(item_id)
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        return jsonify(item.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== PROTECTED ROUTES (Authentication required) ==========

@item_bp.route('/', methods=['POST'])
@jwt_required()
def create_item():
    """
    Create a new item (giver posts something to give away)
    Expected JSON:
    {
        "title": "Sofa Set",
        "description": "Brown leather sofa",
        "photo_url": "https://...",
        "condition": "Good",
        "pickup_location": "Tuskys Roysambu",
        "pickup_days": "Saturdays",
        "pickup_times": "10am-2pm",
        "special_instructions": "Call when you arrive",
        "category_id": 1
    }
    """
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        # Validate required fields
        required_fields = ['title', 'pickup_location', 'category_id']
        missing = [field for field in required_fields if field not in data or not data[field]]
        if missing:
            return jsonify({'error': f'Missing required fields: {", ".join(missing)}'}), 400
        
        # Verify category exists
        category = Category.query.get(data['category_id'])
        if not category:
            return jsonify({'error': 'Invalid category ID'}), 400
        
        # Create new item
        new_item = Item(
            title=data['title'],
            description=data.get('description', ''),
            photo_url=data.get('photo_url', ''),
            condition=data.get('condition', 'Not specified'),
            pickup_location=data['pickup_location'],
            pickup_days=data.get('pickup_days', ''),
            pickup_times=data.get('pickup_times', ''),
            special_instructions=data.get('special_instructions', ''),
            is_available=True,
            giver_id=int(user_id),
            category_id=data['category_id']
        )
        
        db.session.add(new_item)
        db.session.commit()
        
        return jsonify({
            'message': 'Item posted successfully',
            'item': new_item.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@item_bp.route('/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_item(item_id):
    """
    Update an item (only the giver can update)
    """
    try:
        user_id = get_jwt_identity()
        item = Item.query.get(item_id)
        
        # Check if item exists
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        # Check if user is the giver
        if item.giver_id != int(user_id):
            return jsonify({'error': 'You can only update your own items'}), 403
        
        data = request.get_json()
        
        # Update allowed fields
        updatable_fields = ['title', 'description', 'photo_url', 'condition', 
                           'pickup_location', 'pickup_days', 'pickup_times', 
                           'special_instructions', 'category_id', 'is_available']
        
        for field in updatable_fields:
            if field in data:
                setattr(item, field, data[field])
        
        # If category_id is updated, verify it exists
        if 'category_id' in data:
            category = Category.query.get(data['category_id'])
            if not category:
                return jsonify({'error': 'Invalid category ID'}), 400
        
        db.session.commit()
        
        return jsonify({
            'message': 'Item updated successfully',
            'item': item.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@item_bp.route('/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_item(item_id):
    """
    Delete an item (only the giver can delete)
    """
    try:
        user_id = get_jwt_identity()
        item = Item.query.get(item_id)
        
        # Check if item exists
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        # Check if user is the giver
        if item.giver_id != int(user_id):
            return jsonify({'error': 'You can only delete your own items'}), 403
        
        # Check if there are any approved requests
        approved_requests = Request.query.filter_by(item_id=item_id, status='approved').first()
        if approved_requests:
            return jsonify({'error': 'Cannot delete item with approved requests. Mark as given instead.'}), 400
        
        db.session.delete(item)
        db.session.commit()
        
        return jsonify({'message': 'Item deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@item_bp.route('/<int:item_id>/mark-given', methods=['PATCH'])
@jwt_required()
def mark_as_given(item_id):
    """
    Mark item as already given (only the giver can do this)
    """
    try:
        user_id = get_jwt_identity()
        item = Item.query.get(item_id)
        
        # Check if item exists
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        # Check if user is the giver
        if item.giver_id != int(user_id):
            return jsonify({'error': 'You can only mark your own items as given'}), 403
        
        # Update item availability
        item.is_available = False
        
        # Reject all pending requests
        pending_requests = Request.query.filter_by(item_id=item_id, status='pending').all()
        for req in pending_requests:
            req.status = 'rejected'
        
        # Mark any approved request as completed
        approved_request = Request.query.filter_by(item_id=item_id, status='approved').first()
        if approved_request:
            approved_request.status = 'completed'
        
        db.session.commit()
        
        return jsonify({
            'message': 'Item marked as given',
            'item': item.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@item_bp.route('/my-items', methods=['GET'])
@jwt_required()
def get_my_items():
    """
    Get all items posted by the current user
    """
    try:
        user_id = get_jwt_identity()
        items = Item.query.filter_by(giver_id=user_id).order_by(Item.created_at.desc()).all()
        return jsonify([item.to_dict() for item in items]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@item_bp.route('/category/<int:category_id>/items', methods=['GET'])
def get_items_by_category(category_id):
    """
    Get all available items in a specific category
    """
    try:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        
        items = Item.query.filter_by(category_id=category_id, is_available=True).order_by(Item.created_at.desc()).all()
        return jsonify([item.to_dict() for item in items]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500