# routes/dashboard_routes.py
from flask import Blueprint, jsonify
from extensions import db
from models import User, Item, Request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func, extract
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@dashboard_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_user_stats():
    """
    Get user statistics for dashboard
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Items given away (user's items that are no longer available)
        items_given = Item.query.filter_by(giver_id=user_id, is_available=False).count()
        
        # Items currently available
        items_available = Item.query.filter_by(giver_id=user_id, is_available=True).count()
        
        # Total items posted
        total_items = Item.query.filter_by(giver_id=user_id).count()
        
        # Incoming requests (requests on user's items)
        user_item_ids = [item.id for item in user.items]
        incoming_requests_count = Request.query.filter(Request.item_id.in_(user_item_ids)).count()
        
        # Pending incoming requests
        pending_incoming = Request.query.filter(
            Request.item_id.in_(user_item_ids),
            Request.status == 'pending'
        ).count()
        
        # Outgoing requests (requests user made on others' items)
        outgoing_requests_count = Request.query.filter_by(seeker_id=user_id).count()
        
        # Approved outgoing requests
        approved_outgoing = Request.query.filter_by(
            seeker_id=user_id, 
            status='approved'
        ).count()
        
        # Success rate (items received)
        items_received = Request.query.filter_by(
            seeker_id=user_id,
            status='completed'
        ).count()
        
        stats = {
            'as_giver': {
                'total_items': total_items,
                'items_available': items_available,
                'items_given': items_given,
                'incoming_requests': incoming_requests_count,
                'pending_incoming': pending_incoming
            },
            'as_seeker': {
                'outgoing_requests': outgoing_requests_count,
                'approved_requests': approved_outgoing,
                'items_received': items_received
            },
            'impact': {
                'waste_prevented_kg': items_given * 5,  # Rough estimate: 5kg per item
                'people_helped': items_given + items_received
            }
        }
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@dashboard_bp.route('/activity', methods=['GET'])
@jwt_required()
def get_recent_activity():
    """
    Get recent user activity
    """
    try:
        user_id = get_jwt_identity()
        
        # Get user's items
        user_item_ids = [item.id for item in Item.query.filter_by(giver_id=user_id).all()]
        
        # Recent requests on user's items (last 7 days)
        week_ago = datetime.utcnow() - timedelta(days=7)
        
        incoming_activity = Request.query.filter(
            Request.item_id.in_(user_item_ids),
            Request.created_at >= week_ago
        ).order_by(Request.created_at.desc()).limit(5).all()
        
        # User's recent outgoing requests
        outgoing_activity = Request.query.filter_by(
            seeker_id=user_id
        ).filter(
            Request.created_at >= week_ago
        ).order_by(Request.created_at.desc()).limit(5).all()
        
        # Recent items posted by user
        recent_items = Item.query.filter_by(
            giver_id=user_id
        ).filter(
            Item.created_at >= week_ago
        ).order_by(Item.created_at.desc()).limit(5).all()
        
        activity = {
            'incoming_requests': [{
                'id': r.id,
                'message': r.message[:50] + '...' if len(r.message) > 50 else r.message,
                'status': r.status,
                'created_at': r.created_at.isoformat(),
                'seeker_name': r.seeker.name,
                'item_title': r.item.title
            } for r in incoming_activity],
            'outgoing_requests': [{
                'id': r.id,
                'message': r.message[:50] + '...' if len(r.message) > 50 else r.message,
                'status': r.status,
                'created_at': r.created_at.isoformat(),
                'item_title': r.item.title,
                'giver_name': r.giver.name if r.giver else None
            } for r in outgoing_activity],
            'recent_items': [{
                'id': i.id,
                'title': i.title,
                'is_available': i.is_available,
                'created_at': i.created_at.isoformat(),
                'requests_count': len(i.requests)
            } for i in recent_items]
        }
        
        return jsonify(activity), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@dashboard_bp.route('/community-stats', methods=['GET'])
def get_community_stats():
    """
    Get community-wide statistics (public route)
    """
    try:
        # Total items given away
        total_items_given = Item.query.filter_by(is_available=False).count()
        
        # Total active items
        active_items = Item.query.filter_by(is_available=True).count()
        
        # Total users
        total_users = User.query.count()
        
        # Total successful transactions (completed requests)
        successful_transactions = Request.query.filter_by(status='completed').count()
        
        # Items by category
        categories = Category.query.all()
        items_by_category = [{
            'category': cat.name,
            'count': Item.query.filter_by(category_id=cat.id, is_available=True).count()
        } for cat in categories]
        
        # Most active locations
        locations = db.session.query(
            Item.pickup_location, 
            func.count(Item.id).label('count')
        ).filter(Item.is_available==True).group_by(Item.pickup_location).order_by(func.count(Item.id).desc()).limit(5).all()
        
        top_locations = [{'location': loc, 'count': count} for loc, count in locations]
        
        stats = {
            'total_items_given': total_items_given,
            'active_items': active_items,
            'total_users': total_users,
            'successful_transactions': successful_transactions,
            'items_by_category': items_by_category,
            'top_locations': top_locations,
            'estimated_waste_prevented_kg': total_items_given * 5
        }
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500