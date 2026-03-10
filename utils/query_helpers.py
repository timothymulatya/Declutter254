# utils/query_helpers.py
from models import Item, Request, User, Category
from extensions import db
from sqlalchemy import func

def get_popular_categories(limit=5):
    """
    Get most popular categories based on item count
    """
    categories = db.session.query(
        Category.id,
        Category.name,
        func.count(Item.id).label('item_count')
    ).outerjoin(Item, Item.category_id == Category.id)\
     .filter(Item.is_available == True)\
     .group_by(Category.id)\
     .order_by(func.count(Item.id).desc())\
     .limit(limit)\
     .all()
    
    return [{'id': c.id, 'name': c.name, 'count': c.item_count} for c in categories]

def get_recent_items(limit=10):
    """
    Get most recently posted available items
    """
    items = Item.query.filter_by(is_available=True)\
                      .order_by(Item.created_at.desc())\
                      .limit(limit)\
                      .all()
    return items

def get_user_impact_stats(user_id):
    """
    Get impact statistics for a user
    - Items given away
    - Items received
    - People helped (estimated)
    """
    # Items given (user as giver, item marked unavailable)
    items_given = Item.query.filter_by(giver_id=user_id, is_available=False).count()
    
    # Items received (user as seeker, request completed)
    items_received = Request.query.filter_by(
        seeker_id=user_id, 
        status='completed'
    ).count()
    
    # People helped (unique seekers who got user's items)
    user_item_ids = [item.id for item in Item.query.filter_by(giver_id=user_id).all()]
    
    unique_helped = 0
    if user_item_ids:
        unique_helped = db.session.query(func.count(func.distinct(Request.seeker_id)))\
                                   .filter(Request.item_id.in_(user_item_ids))\
                                   .filter(Request.status == 'completed')\
                                   .scalar()
    
    return {
        'items_given': items_given,
        'items_received': items_received,
        'unique_people_helped': unique_helped or 0,
        'total_items_shared': items_given + items_received
    }

def check_item_availability(item_id):
    """
    Check if an item is available and return status with message
    """
    item = Item.query.get(item_id)
    
    if not item:
        return {'available': False, 'reason': 'not_found', 'message': 'Item not found'}
    
    if not item.is_available:
        return {'available': False, 'reason': 'already_given', 'message': 'This item has already been given away'}
    
    # Check if there's an approved request
    approved = Request.query.filter_by(item_id=item_id, status='approved').first()
    if approved:
        return {'available': False, 'reason': 'pending_pickup', 'message': 'This item is already committed to someone else'}
    
    return {'available': True, 'reason': None, 'message': 'Item is available'}

def get_items_by_location(location, limit=20):
    """
    Get items near a specific location
    """
    items = Item.query.filter(
        Item.pickup_location.ilike(f'%{location}%'),
        Item.is_available == True
    ).order_by(Item.created_at.desc()).limit(limit).all()
    
    return items