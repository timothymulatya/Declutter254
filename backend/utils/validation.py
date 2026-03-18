# utils/validation.py
from backend.models import Category, Item

def validate_item(data):
    """Validate item data before saving"""
    errors = []
    
    # Title validation
    if not data.get('title'):
        errors.append("Title is required")
    elif len(data['title']) < 3:
        errors.append("Title must be at least 3 characters")
    elif len(data['title']) > 100:
        errors.append("Title must be less than 100 characters")
    
    # Location validation
    if not data.get('pickup_location'):
        errors.append("Pickup location is required")
    
    # Category validation
    if not data.get('category_id'):
        errors.append("Category is required")
    else:
        if not Category.query.get(data['category_id']):
            errors.append("Category does not exist")
    
    # Condition validation (if provided)
    valid_conditions = ['Like New', 'Good', 'Fair', 'Needs Repair']
    if data.get('condition') and data['condition'] not in valid_conditions:
        errors.append(f"Condition must be one of: {', '.join(valid_conditions)}")
    
    return errors

def validate_request(data):
    """Validate request message"""
    errors = []
    
    if not data.get('message'):
        errors.append("Please explain why you need this item")
    elif len(data['message']) < 10:
        errors.append("Please provide more detail (at least 10 characters)")
    elif len(data['message']) > 500:
        errors.append("Message is too long (max 500 characters)")
    
    return errors

def validate_phone(phone):
    """Validate Kenyan phone number"""
    from backend.utils.validators import validate_kenyan_phone
    return validate_kenyan_phone(phone) is not None
