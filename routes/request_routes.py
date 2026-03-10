# routes/request_routes.py
from flask import Blueprint, request, jsonify
from extensions import db
from models import Request, Item, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

request_bp = Blueprint('requests', __name__, url_prefix='/api/requests')

@request_bp.route('/item/<int:item_id>', methods=['POST'])
@jwt_required()
def create_request(item_id):
    """Create a new request for an item"""
    try:
        data = request.get_json()
        seeker_id = get_jwt_identity()

        if not data or 'message' not in data or not data['message']:
            return jsonify({'error': 'Please explain why you need this item'}), 400

        if len(data['message']) < 10:
            return jsonify({'error': 'Please provide a more detailed explanation (at least 10 characters)'}), 400

        item = Item.query.get(item_id)
        if not item:
            return jsonify({'error': 'Item not found'}), 404

        if not item.is_available:
            return jsonify({'error': 'This item is no longer available'}), 400

        if item.giver_id == int(seeker_id):
            return jsonify({'error': 'You cannot request your own item'}), 400

        existing_request = Request.query.filter_by(
            item_id=item_id,
            seeker_id=seeker_id,
            status='pending'
        ).first()

        if existing_request:
            return jsonify({'error': 'You already have a pending request for this item'}), 400

        new_request = Request(
            message=data['message'],
            status='pending',
            seeker_id=int(seeker_id),
            item_id=item_id
        )

        db.session.add(new_request)
        db.session.commit()

        return jsonify({
            'message': 'Request sent successfully',
            'request': new_request.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@request_bp.route('/<int:request_id>', methods=['GET'])
@jwt_required()
def get_request(request_id):
    """
    Get a single request by ID
    Only accessible by the seeker or the giver of the item
    """
    try:
        user_id = get_jwt_identity()
        request_item = Request.query.get(request_id)
        
        if not request_item:
            return jsonify({'error': 'Request not found'}), 404
        
        # Check if user is either the seeker or the giver
        is_seeker = request_item.seeker_id == int(user_id)
        is_giver = request_item.item.giver_id == int(user_id)
        
        if not (is_seeker or is_giver):
            return jsonify({'error': 'You can only view your own requests'}), 403
        
        return jsonify(request_item.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@request_bp.route('/', methods=['GET'])
@jwt_required()
def get_requests():
    """
    Get all requests with optional filtering
    Query parameters:
    - status: filter by status (pending, approved, rejected)
    - item_id: filter by specific item
    - role: 'giver' or 'seeker' to filter by user's role
    """
    try:
        user_id = get_jwt_identity()
        status = request.args.get('status')
        item_id = request.args.get('item_id')
        role = request.args.get('role')
        
        query = Request.query
        
        # Filter by status
        if status:
            query = query.filter_by(status=status)
        
        # Filter by specific item
        if item_id:
            query = query.filter_by(item_id=item_id)
        
        # Filter by user's role
        if role == 'giver':
            # Get items belonging to current user
            user_items = Item.query.filter_by(giver_id=user_id).all()
            item_ids = [item.id for item in user_items]
            query = query.filter(Request.item_id.in_(item_ids))
        elif role == 'seeker':
            query = query.filter_by(seeker_id=user_id)
        else:
            # Default: show both incoming and outgoing
            user_items = Item.query.filter_by(giver_id=user_id).all()
            item_ids = [item.id for item in user_items]
            query = query.filter(
                (Request.seeker_id == user_id) | 
                (Request.item_id.in_(item_ids))
            )
        
        # Order by newest first
        requests_list = query.order_by(Request.created_at.desc()).all()
        
        return jsonify([req.to_dict() for req in requests_list]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@request_bp.route('/incoming', methods=['GET'])
@jwt_required()
def get_incoming_requests():
    """Get all requests for items that the current user is giving away"""
    try:
        user_id = get_jwt_identity()
        user_items = Item.query.filter_by(giver_id=user_id).all()
        item_ids = [item.id for item in user_items]

        requests_list = Request.query.filter(
            Request.item_id.in_(item_ids)
        ).order_by(Request.created_at.desc()).all()

        return jsonify([req.to_dict() for req in requests_list]), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@request_bp.route('/outgoing', methods=['GET'])
@jwt_required()
def get_outgoing_requests():
    """Get all requests made by the current user"""
    try:
        user_id = get_jwt_identity()
        requests_list = Request.query.filter_by(seeker_id=user_id).order_by(Request.created_at.desc()).all()
        return jsonify([req.to_dict() for req in requests_list]), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@request_bp.route('/<int:request_id>/approve', methods=['PATCH'])
@jwt_required()
def approve_request(request_id):
    """Approve a request - reveals phone number"""
    try:
        user_id = get_jwt_identity()
        request_item = Request.query.get(request_id)

        if not request_item:
            return jsonify({'error': 'Request not found'}), 404

        if request_item.item.giver_id != int(user_id):
            return jsonify({'error': 'You can only approve requests for your own items'}), 403

        if request_item.status != 'pending':
            return jsonify({'error': f'This request is already {request_item.status}'}), 400

        if not request_item.item.is_available:
            return jsonify({'error': 'This item is no longer available'}), 400

        request_item.status = 'approved'

        # Reject all other pending requests for this item
        other_requests = Request.query.filter(
            Request.item_id == request_item.item_id,
            Request.id != request_id,
            Request.status == 'pending'
        ).all()

        for req in other_requests:
            req.status = 'rejected'

        db.session.commit()

        return jsonify({
            'message': 'Request approved successfully. Phone number revealed.',
            'request': request_item.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@request_bp.route('/<int:request_id>/reject', methods=['PATCH'])
@jwt_required()
def reject_request(request_id):
    """Reject a request"""
    try:
        user_id = get_jwt_identity()
        request_item = Request.query.get(request_id)

        if not request_item:
            return jsonify({'error': 'Request not found'}), 404

        if request_item.item.giver_id != int(user_id):
            return jsonify({'error': 'You can only reject requests for your own items'}), 403

        if request_item.status != 'pending':
            return jsonify({'error': f'This request is already {request_item.status}'}), 400

        request_item.status = 'rejected'
        db.session.commit()

        return jsonify({
            'message': 'Request rejected',
            'request': request_item.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500