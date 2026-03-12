# models.py - CLEAN MVP VERSION
from extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships 
    items = db.relationship('Item', back_populates='giver', cascade='all, delete-orphan')
    outgoing_requests = db.relationship('Request', 
                                       foreign_keys='Request.seeker_id', 
                                       back_populates='seeker',
                                       cascade='all, delete-orphan')
    

    
    def __repr__(self):
        return f'<User: {self.name} ({self.phone_number})>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone_number': self.phone_number,
            'location': self.location,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'items_count': len(self.items) if self.items else 0
           
        }


class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    
    # Relationships
    items = db.relationship('Item', back_populates='category')
    
    
    
    def __repr__(self):
        return f'<Category: {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'items_count': len(self.items) if self.items else 0
        }


class Item(db.Model):
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    photo_url = db.Column(db.String(500))
    condition = db.Column(db.String(50))
    pickup_location = db.Column(db.String(200), nullable=False)
    pickup_days = db.Column(db.String(100))
    pickup_times = db.Column(db.String(100))
    special_instructions = db.Column(db.Text)
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    giver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    
    # Relationships
    giver = db.relationship('User', back_populates='items')
    category = db.relationship('Category', back_populates='items')
    requests = db.relationship('Request', 
                              foreign_keys='Request.item_id',
                              back_populates='item',
                              cascade='all, delete-orphan')
    
    
    def __repr__(self):
        return f'<Item: {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'photo_url': self.photo_url,
            'condition': self.condition,
            'pickup_location': self.pickup_location,
            'pickup_days': self.pickup_days,
            'pickup_times': self.pickup_times,
            'special_instructions': self.special_instructions,
            'is_available': self.is_available,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'giver_id': self.giver_id,
            'giver_name': self.giver.name if self.giver else None,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'requests_count': len([r for r in self.requests if r.status == 'pending']) if self.requests else 0
        }


class Request(db.Model):
    __tablename__ = 'requests'
    
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)  # USER-SUBMITTABLE ATTRIBUTE
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    seeker_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    
    # Relationships
    seeker = db.relationship('User', foreign_keys=[seeker_id], back_populates='outgoing_requests')
    item = db.relationship('Item', foreign_keys=[item_id], back_populates='requests')
    
   
    
    @property
    def giver(self):
        return self.item.giver if self.item else None
    
    @property
    def giver_phone(self):
        """Only reveal phone if request is approved"""
        if self.status == 'approved' and self.item and self.item.giver:
            return self.item.giver.phone_number
        return None
    
    def __repr__(self):
        return f'<Request: {self.seeker.name if self.seeker else "Unknown"} -> {self.item.title if self.item else "Unknown"}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'message': self.message,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'seeker_id': self.seeker_id,
            'seeker_name': self.seeker.name if self.seeker else None,
            'item_id': self.item_id,
            'item_title': self.item.title if self.item else None,
            'giver_name': self.giver.name if self.giver else None,
            'giver_phone': self.giver_phone
        }

