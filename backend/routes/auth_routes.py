from flask import Blueprint, request, jsonify
from backend.extensions import db, migrate, cors, bcrypt, jwt
from backend.config import Config
from backend.utils.validators import validate_kenyan_phone, validate_required_fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['phone_number', 'password', 'name']
        missing = validate_required_fields(data, required_fields)
        if missing:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing)}'
            }), 400
        
        # Validate Kenyan phone number
        phone = validate_kenyan_phone(data['phone_number'])
        if not phone:
            return jsonify({
                'error': 'Invalid Kenyan phone number. Use 07XXXXXXXX or 01XXXXXXXX format'
            }), 400
        
        # Check if user already exists
        existing_user = User.query.filter_by(phone_number=phone).first()
        if existing_user:
            return jsonify({
                'error': 'Phone number already registered'
            }), 409
        
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        
        # Create new user
        new_user = User(
            phone_number=phone,
            password_hash=hashed_password,
            name=data['name'],
            location=data.get('location', '')
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Create access token - ensure identity is a string
        access_token = create_access_token(
            identity=str(new_user.id),
            expires_delta=timedelta(hours=24)
        )
        
        return jsonify({
            'message': 'User registered successfully',
            'token': access_token,
            'user': new_user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        missing = validate_required_fields(data, ['phone_number', 'password'])
        if missing:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing)}'
            }), 400
        
        # Validate and normalize phone number
        phone = validate_kenyan_phone(data['phone_number'])
        if not phone:
            return jsonify({
                'error': 'Invalid Kenyan phone number'
            }), 400
        
        # Find user
        user = User.query.filter_by(phone_number=phone).first()
        
        # Check if user exists and password is correct
        if not user or not bcrypt.check_password_hash(user.password_hash, data['password']):
            return jsonify({
                'error': 'Invalid phone number or password'
            }), 401
        
        # Create access token - ensure identity is a string
        access_token = create_access_token(
            identity=str(user.id),
            expires_delta=timedelta(hours=24)
        )
        
        return jsonify({
            'message': 'Login successful',
            'token': access_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """
    Get current user's profile (protected route)
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))  # Convert to int for query
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(user.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """
    Update user profile (protected route)
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        if 'name' in data:
            user.name = data['name']
        if 'location' in data:
            user.location = data['location']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500