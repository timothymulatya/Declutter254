# utils/validators.py
import re

def validate_kenyan_phone(phone_number):
    """
    Validate Kenyan phone numbers.
    Formats accepted:
    - 0712345678
    - 0112345678
    - 254712345678
    - +254712345678
    """
    # Remove any spaces, dashes, or parentheses
    phone = re.sub(r'[\s\-\(\)]', '', phone_number)
    
    # Kenyan phone regex patterns
    patterns = [
        r'^07\d{8}$',           # 0712345678
        r'^01\d{8}$',           # 0112345678
        r'^2547\d{8}$',         # 254712345678
        r'^2541\d{8}$',         # 254112345678
        r'^\+2547\d{8}$',       # +254712345678
        r'^\+2541\d{8}$'        # +254112345678
    ]
    
    for pattern in patterns:
        if re.match(pattern, phone):
            # Normalize to 07 format for storage
            if phone.startswith('254'):
                phone = '0' + phone[3:]
            elif phone.startswith('+254'):
                phone = '0' + phone[4:]
            return phone
    
    return None

def validate_required_fields(data, required_fields):
    """
    Validate that all required fields are present and not empty.
    """
    missing_fields = []
    for field in required_fields:
        if field not in data or not data[field]:
            missing_fields.append(field)
    
    return missing_fields

def validate_email(email):
    """
    Basic email validation (if we add email later)
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None