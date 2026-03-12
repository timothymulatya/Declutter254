DECLUTTER254 - PROJECT HANDOFF DOCUMENTATION
FROM: Team Member 1 (Backend Lead)
TO: Team Members 2, 3, and 4
TABLE OF CONTENTS
Project Overview

What I've Completed (Team Member 1)

Team Member 2 Tasks - Backend API Developer

Team Member 3 Tasks - Frontend Lead

Team Member 4 Tasks - Frontend Features Developer

GitHub Workflow

API Documentation Reference

1. PROJECT OVERVIEW
Declutter254
A Kenyan-made platform connecting people who have extra items with those who need them.

Tech Stack
Backend: Flask + SQLAlchemy + JWT Authentication

Frontend: React + React Router + Formik

Database: SQLite (development) / PostgreSQL (production)

Authentication: JWT tokens with phone number validation

GitHub Repository
text
https://github.com/Benjakusa/Declutter254.git
2. WHAT I'VE COMPLETED (TEAM MEMBER 1)
2.1 Backend Foundation
Flask application with factory pattern

Database configuration and migrations setup

CORS enabled for React frontend

Environment variables configuration

All dependencies in requirements.txt

2.2 Database Models
text
# Complete MVP Models
- User     (id, phone_number, password_hash, name, location, created_at)
- Category (id, name, description)
- Item     (id, title, description, photo_url, condition, pickup_location, 
            pickup_days, pickup_times, special_instructions, is_available, 
            created_at, giver_id, category_id)
- Request  (id, message, status, created_at, seeker_id, item_id)

# Relationships Established
- One-to-Many: User → Items
- One-to-Many: Category → Items  
- Many-to-Many: User ↔ Item through Request (with 'message' as user-submittable)
2.3 Authentication System
Kenyan phone validation (supports 07..., 01..., 254..., +254...)

Password hashing with bcrypt

JWT token generation and validation

Protected routes with @jwt_required()

User registration and login endpoints

2.4 Completed API Endpoints
Method	Endpoint	Description	Status
POST	/api/auth/register	Register new user	Done
POST	/api/auth/login	Login user	Done
GET	/api/auth/profile	Get user profile	Done
PUT	/api/auth/profile	Update profile	Done
GET	/api/categories/	Get all categories	Done
GET	/api/categories/<id>	Get single category	Done
POST	/api/categories/	Create category	Done
GET	/api/items/	Get all items (with filters)	Done
GET	/api/items/<id>	Get single item	Done
POST	/api/items/	Create new item	Done
PUT	/api/items/<id>	Update item	Done
DELETE	/api/items/<id>	Delete item	Done
GET	/api/items/my-items	Get user's items	Done
PATCH	/api/items/<id>/mark-given	Mark item as given	Done
POST	/api/requests/item/<id>	Create request	Done
GET	/api/requests/incoming	Get requests on my items	Done
GET	/api/requests/outgoing	Get my requests	Done
PATCH	/api/requests/<id>/approve	Approve request	Done
PATCH	/api/requests/<id>/reject	Reject request	Done
2.5 Documentation Created
Complete API documentation with examples

Postman collection (optional)

This handoff document

3. TEAM MEMBER 2 TASKS - BACKEND API DEVELOPER
Your Role: Enhance and optimize the backend API
Files You'll Work With:
text
routes/item_routes.py
routes/request_routes.py
models.py
utils/validation.py (you'll create this)
tests/test_items.py (you'll create this)
tests/test_requests.py (you'll create this)
Task 1: Add Pagination to Items Listing (Priority: HIGH)
Location: routes/item_routes.py - get_items() function

What to do:
Add pagination parameters so frontend can load items in batches.

Code to add:

python
# Add these parameters to the function
page = request.args.get('page', 1, type=int)
per_page = request.args.get('per_page', 10, type=int)

# Modify the query
paginated = query.order_by(Item.created_at.desc()).paginate(
    page=page, 
    per_page=per_page,
    error_out=False
)

# Return with metadata
return jsonify({
    'items': [item.to_dict() for item in paginated.items],
    'total': paginated.total,
    'pages': paginated.pages,
    'current_page': page,
    'per_page': per_page,
    'has_next': paginated.has_next,
    'has_prev': paginated.has_prev
}), 200
Testing:

bash
# Test pagination
curl "http://localhost:5555/api/items/?page=2&per_page=5"
Task 2: Create Input Validation Utilities (Priority: HIGH)
Create file: utils/validation.py

What to do:
Create reusable validation functions for all inputs.

Code to add:

python
# utils/validation.py
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
        from models import Category
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
    from utils.validators import validate_kenyan_phone
    return validate_kenyan_phone(phone) is not None
Use in routes:

python
from utils.validation import validate_item, validate_request

# In create_item route
errors = validate_item(data)
if errors:
    return jsonify({'errors': errors}), 400
Task 3: Add Sorting Options (Priority: MEDIUM)
Location: routes/item_routes.py - get_items() function

What to do:
Allow users to sort items by different criteria.

Code to add:

python
# Get sort parameter
sort_by = request.args.get('sort', 'newest')

# Apply sorting
if sort_by == 'newest':
    query = query.order_by(Item.created_at.desc())
elif sort_by == 'oldest':
    query = query.order_by(Item.created_at.asc())
elif sort_by == 'title':
    query = query.order_by(Item.title.asc())
elif sort_by == 'popular':
    # Sort by number of requests
    from sqlalchemy import func
    query = query.outerjoin(Request).group_by(Item.id).order_by(func.count(Request.id).desc())
Testing:

bash
curl "http://localhost:5555/api/items/?sort=title"
Task 4: Add Request Count to Item Details (Priority: LOW)
Location: models.py - Item.to_dict() method

What to do:
Add pending requests count to help givers see interest.

Code to add:

python
# In the to_dict method, add:
'pending_requests_count': len([r for r in self.requests if r.status == 'pending']) if self.requests else 0,
'approved_requests_count': len([r for r in self.requests if r.status == 'approved']) if self.requests else 0,
Task 5: Write Unit Tests (Priority: MEDIUM)
Create files:

tests/test_items.py

tests/test_requests.py

Sample test file:

python
# tests/test_items.py
import unittest
from app import create_app, db
from models import User, Category, Item

class ItemTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            # Create test data
            category = Category(name="Test", description="Test")
            db.session.add(category)
            db.session.commit()
    
    def test_get_items(self):
        response = self.client.get('/api/items/')
        self.assertEqual(response.status_code, 200)
    
    def test_create_item_requires_auth(self):
        response = self.client.post('/api/items/', json={})
        self.assertEqual(response.status_code, 401)
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main()
4. TEAM MEMBER 3 TASKS - FRONTEND LEAD
Your Role: Set up React application, routing, and core components
Task 1: Initialize React Application
bash
# Create React app
npx create-react-app declutter254-frontend
cd declutter254-frontend

# Install dependencies
npm install react-router-dom@6 formik yup axios
npm install bootstrap react-bootstrap  # Optional for styling
npm install react-icons  # For icons

# Start development server
npm start
Task 2: Create Folder Structure
text
src/
├── components/
│   ├── NavBar.js
│   ├── PrivateRoute.js
│   ├── LoadingSpinner.js
│   └── ErrorMessage.js
├── pages/
│   ├── HomePage.js
│   ├── ItemDetailPage.js
│   ├── PostItemPage.js
│   ├── ProfilePage.js
│   ├── RequestsPage.js
│   ├── LoginPage.js
│   └── SignupPage.js
├── context/
│   └── AuthContext.js
├── services/
│   ├── api.js
│   └── auth.js
├── utils/
│   └── validators.js
├── App.js
├── index.js
└── styles.css
Task 3: Create Authentication Context
File: src/context/AuthContext.js

javascript
import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);

  // Set axios default header
  if (token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  }

  const login = async (phone_number, password) => {
    try {
      const response = await axios.post('http://localhost:5555/api/auth/login', {
        phone_number,
        password
      });
      const { token, user } = response.data;
      localStorage.setItem('token', token);
      setToken(token);
      setUser(user);
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      return { success: true };
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.error || 'Login failed' 
      };
    }
  };

  const register = async (userData) => {
    try {
      const response = await axios.post('http://localhost:5555/api/auth/register', userData);
      const { token, user } = response.data;
      localStorage.setItem('token', token);
      setToken(token);
      setUser(user);
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      return { success: true };
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.error || 'Registration failed' 
      };
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
    delete axios.defaults.headers.common['Authorization'];
  };

  const fetchProfile = async () => {
    try {
      const response = await axios.get('http://localhost:5555/api/auth/profile');
      setUser(response.data);
    } catch (error) {
      console.error('Failed to fetch profile:', error);
      if (error.response?.status === 401) {
        logout();
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (token) {
      fetchProfile();
    } else {
      setLoading(false);
    }
  }, [token]);

  const value = {
    user,
    token,
    loading,
    login,
    register,
    logout
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
Task 4: Create Navigation Bar
File: src/components/NavBar.js

javascript
import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const NavBar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav style={{
      display: 'flex',
      justifyContent: 'space-between',
      padding: '1rem 2rem',
      backgroundColor: '#f8f9fa',
      borderBottom: '1px solid #dee2e6'
    }}>
      <div>
        <Link to="/" style={{ marginRight: '1rem', fontWeight: 'bold' }}>
          Declutter254
        </Link>
        <Link to="/" style={{ marginRight: '1rem' }}>Home</Link>
        {user && (
          <>
            <Link to="/post-item" style={{ marginRight: '1rem' }}>Post Item</Link>
            <Link to="/requests" style={{ marginRight: '1rem' }}>Requests</Link>
            <Link to="/profile" style={{ marginRight: '1rem' }}>Profile</Link>
          </>
        )}
      </div>
      <div>
        {user ? (
          <>
            <span style={{ marginRight: '1rem' }}>Hello, {user.name}</span>
            <button onClick={handleLogout}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login" style={{ marginRight: '1rem' }}>Login</Link>
            <Link to="/signup">Sign Up</Link>
          </>
        )}
      </div>
    </nav>
  );
};

export default NavBar;
Task 5: Create API Service
File: src/services/api.js

javascript
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5555/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add token to requests if it exists
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

// Handle response errors
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Items API
export const getItems = (params) => api.get('/items/', { params });
export const getItem = (id) => api.get(`/items/${id}`);
export const createItem = (data) => api.post('/items/', data);
export const updateItem = (id, data) => api.put(`/items/${id}`, data);
export const deleteItem = (id) => api.delete(`/items/${id}`);
export const getMyItems = () => api.get('/items/my-items');
export const markItemAsGiven = (id) => api.patch(`/items/${id}/mark-given`);

// Categories API
export const getCategories = () => api.get('/categories/');

// Requests API
export const createRequest = (itemId, message) => 
  api.post(`/requests/item/${itemId}`, { message });
export const getIncomingRequests = () => api.get('/requests/incoming');
export const getOutgoingRequests = () => api.get('/requests/outgoing');
export const approveRequest = (id) => api.patch(`/requests/${id}/approve`);
export const rejectRequest = (id) => api.patch(`/requests/${id}/reject`);

export default api;
Task 6: Set Up React Router
File: src/App.js

javascript
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import NavBar from './components/NavBar';
import PrivateRoute from './components/PrivateRoute';
import HomePage from './pages/HomePage';
import ItemDetailPage from './pages/ItemDetailPage';
import PostItemPage from './pages/PostItemPage';
import ProfilePage from './pages/ProfilePage';
import RequestsPage from './pages/RequestsPage';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignupPage';
import './styles.css';

function AppRoutes() {
  const { loading } = useAuth();

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <BrowserRouter>
      <NavBar />
      <div className="container">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/items/:id" element={<ItemDetailPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route path="/post-item" element={
            <PrivateRoute>
              <PostItemPage />
            </PrivateRoute>
          } />
          <Route path="/profile" element={
            <PrivateRoute>
              <ProfilePage />
            </PrivateRoute>
          } />
          <Route path="/requests" element={
            <PrivateRoute>
              <RequestsPage />
            </PrivateRoute>
          } />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  );
}

export default App;
Task 7: Create PrivateRoute Component
File: src/components/PrivateRoute.js

javascript
import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const PrivateRoute = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return <div>Loading...</div>;
  }

  return user ? children : <Navigate to="/login" />;
};

export default PrivateRoute;
5. TEAM MEMBER 4 TASKS - FRONTEND FEATURES DEVELOPER
Your Role: Build forms, fetch integration, and interactive features
Task 1: Create HomePage with Items Grid
File: src/pages/HomePage.js

javascript
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getItems, getCategories } from '../services/api';

const HomePage = () => {
  const [items, setItems] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    category: '',
    location: '',
    search: ''
  });

  useEffect(() => {
    fetchCategories();
    fetchItems();
  }, []);

  useEffect(() => {
    fetchItems();
  }, [filters]);

  const fetchCategories = async () => {
    try {
      const response = await getCategories();
      setCategories(response.data);
    } catch (error) {
      console.error('Failed to fetch categories:', error);
    }
  };

  const fetchItems = async () => {
    setLoading(true);
    try {
      const params = {};
      if (filters.category) params.category = filters.category;
      if (filters.location) params.location = filters.location;
      if (filters.search) params.search = filters.search;
      
      const response = await getItems(params);
      setItems(response.data);
    } catch (error) {
      console.error('Failed to fetch items:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (e) => {
    setFilters({
      ...filters,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div>
      <h1>Available Items</h1>
      
      {/* Search and Filter Bar */}
      <div style={{ marginBottom: '2rem', display: 'flex', gap: '1rem' }}>
        <input
          type="text"
          name="search"
          placeholder="Search items..."
          value={filters.search}
          onChange={handleFilterChange}
          style={{ flex: 2, padding: '0.5rem' }}
        />
        
        <select
          name="category"
          value={filters.category}
          onChange={handleFilterChange}
          style={{ flex: 1, padding: '0.5rem' }}
        >
          <option value="">All Categories</option>
          {categories.map(cat => (
            <option key={cat.id} value={cat.id}>{cat.name}</option>
          ))}
        </select>
        
        <input
          type="text"
          name="location"
          placeholder="Location..."
          value={filters.location}
          onChange={handleFilterChange}
          style={{ flex: 1, padding: '0.5rem' }}
        />
      </div>

      {/* Items Grid */}
      {loading ? (
        <div>Loading...</div>
      ) : items.length === 0 ? (
        <div>No items found</div>
      ) : (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
          gap: '1rem'
        }}>
          {items.map(item => (
            <Link to={`/items/${item.id}`} key={item.id} style={{ textDecoration: 'none', color: 'inherit' }}>
              <div style={{
                border: '1px solid #ddd',
                borderRadius: '8px',
                overflow: 'hidden',
                padding: '1rem'
              }}>
                {item.photo_url && (
                  <img 
                    src={item.photo_url} 
                    alt={item.title}
                    style={{ width: '100%', height: '200px', objectFit: 'cover' }}
                  />
                )}
                <h3>{item.title}</h3>
                <p>{item.description?.substring(0, 100)}...</p>
                <p><strong>Location:</strong> {item.pickup_location}</p>
                <p><strong>Condition:</strong> {item.condition}</p>
                <span style={{
                  backgroundColor: item.is_available ? '#4CAF50' : '#f44336',
                  color: 'white',
                  padding: '0.25rem 0.5rem',
                  borderRadius: '4px'
                }}>
                  {item.is_available ? 'Available' : 'Given Away'}
                </span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
};

export default HomePage;
Task 2: Create Login Page with Formik
File: src/pages/LoginPage.js

javascript
import React from 'react';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const LoginSchema = Yup.object({
  phone_number: Yup.string()
    .required('Phone number is required')
    .matches(/^(07|01)\d{8}$/, 'Must be a valid Kenyan phone number (e.g., 0712345678)'),
  password: Yup.string()
    .required('Password is required')
    .min(6, 'Password must be at least 6 characters')
});

const LoginPage = () => {
  const navigate = useNavigate();
  const { login } = useAuth();

  const formik = useFormik({
    initialValues: {
      phone_number: '',
      password: ''
    },
    validationSchema: LoginSchema,
    onSubmit: async (values, { setSubmitting, setErrors }) => {
      const result = await login(values.phone_number, values.password);
      if (result.success) {
        navigate('/');
      } else {
        setErrors({ general: result.error });
      }
      setSubmitting(false);
    }
  });

  return (
    <div style={{ maxWidth: '400px', margin: '2rem auto' }}>
      <h2>Login to Declutter254</h2>
      
      {formik.errors.general && (
        <div style={{ color: 'red', marginBottom: '1rem' }}>
          {formik.errors.general}
        </div>
      )}
      
      <form onSubmit={formik.handleSubmit}>
        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="phone_number">Phone Number</label>
          <input
            id="phone_number"
            name="phone_number"
            type="text"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.phone_number}
            style={{ width: '100%', padding: '0.5rem' }}
            placeholder="0712345678"
          />
          {formik.touched.phone_number && formik.errors.phone_number && (
            <div style={{ color: 'red', fontSize: '0.875rem' }}>
              {formik.errors.phone_number}
            </div>
          )}
        </div>

        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="password">Password</label>
          <input
            id="password"
            name="password"
            type="password"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.password}
            style={{ width: '100%', padding: '0.5rem' }}
          />
          {formik.touched.password && formik.errors.password && (
            <div style={{ color: 'red', fontSize: '0.875rem' }}>
              {formik.errors.password}
            </div>
          )}
        </div>

        <button
          type="submit"
          disabled={formik.isSubmitting}
          style={{
            width: '100%',
            padding: '0.75rem',
            backgroundColor: '#4CAF50',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          {formik.isSubmitting ? 'Logging in...' : 'Login'}
        </button>
      </form>
      
      <p style={{ marginTop: '1rem', textAlign: 'center' }}>
        Don't have an account? <Link to="/signup">Sign up</Link>
      </p>
    </div>
  );
};

export default LoginPage;
Task 3: Create Signup Page with Formik
File: src/pages/SignupPage.js

javascript
import React from 'react';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const SignupSchema = Yup.object({
  name: Yup.string()
    .required('Name is required')
    .min(2, 'Name must be at least 2 characters'),
  phone_number: Yup.string()
    .required('Phone number is required')
    .matches(/^(07|01)\d{8}$/, 'Must be a valid Kenyan phone number (e.g., 0712345678)'),
  password: Yup.string()
    .required('Password is required')
    .min(6, 'Password must be at least 6 characters'),
  confirm_password: Yup.string()
    .oneOf([Yup.ref('password'), null], 'Passwords must match')
    .required('Please confirm your password'),
  location: Yup.string()
});

const SignupPage = () => {
  const navigate = useNavigate();
  const { register } = useAuth();

  const formik = useFormik({
    initialValues: {
      name: '',
      phone_number: '',
      password: '',
      confirm_password: '',
      location: ''
    },
    validationSchema: SignupSchema,
    onSubmit: async (values, { setSubmitting, setErrors }) => {
      const { confirm_password, ...userData } = values;
      const result = await register(userData);
      if (result.success) {
        navigate('/');
      } else {
        setErrors({ general: result.error });
      }
      setSubmitting(false);
    }
  });

  return (
    <div style={{ maxWidth: '400px', margin: '2rem auto' }}>
      <h2>Create an Account</h2>
      
      {formik.errors.general && (
        <div style={{ color: 'red', marginBottom: '1rem' }}>
          {formik.errors.general}
        </div>
      )}
      
      <form onSubmit={formik.handleSubmit}>
        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="name">Full Name</label>
          <input
            id="name"
            name="name"
            type="text"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.name}
            style={{ width: '100%', padding: '0.5rem' }}
          />
          {formik.touched.name && formik.errors.name && (
            <div style={{ color: 'red', fontSize: '0.875rem' }}>
              {formik.errors.name}
            </div>
          )}
        </div>

        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="phone_number">Phone Number</label>
          <input
            id="phone_number"
            name="phone_number"
            type="text"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.phone_number}
            style={{ width: '100%', padding: '0.5rem' }}
            placeholder="0712345678"
          />
          {formik.touched.phone_number && formik.errors.phone_number && (
            <div style={{ color: 'red', fontSize: '0.875rem' }}>
              {formik.errors.phone_number}
            </div>
          )}
        </div>

        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="location">Location (optional)</label>
          <input
            id="location"
            name="location"
            type="text"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.location}
            style={{ width: '100%', padding: '0.5rem' }}
            placeholder="e.g., Roysambu, Nairobi"
          />
        </div>

        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="password">Password</label>
          <input
            id="password"
            name="password"
            type="password"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.password}
            style={{ width: '100%', padding: '0.5rem' }}
          />
          {formik.touched.password && formik.errors.password && (
            <div style={{ color: 'red', fontSize: '0.875rem' }}>
              {formik.errors.password}
            </div>
          )}
        </div>

        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="confirm_password">Confirm Password</label>
          <input
            id="confirm_password"
            name="confirm_password"
            type="password"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.confirm_password}
            style={{ width: '100%', padding: '0.5rem' }}
          />
          {formik.touched.confirm_password && formik.errors.confirm_password && (
            <div style={{ color: 'red', fontSize: '0.875rem' }}>
              {formik.errors.confirm_password}
            </div>
          )}
        </div>

        <button
          type="submit"
          disabled={formik.isSubmitting}
          style={{
            width: '100%',
            padding: '0.75rem',
            backgroundColor: '#4CAF50',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          {formik.isSubmitting ? 'Creating account...' : 'Sign Up'}
        </button>
      </form>
      
      <p style={{ marginTop: '1rem', textAlign: 'center' }}>
        Already have an account? <Link to="/login">Login</Link>
      </p>
    </div>
  );
};

export default SignupPage;
Task 4: Create Post Item Form
File: src/pages/PostItemPage.js

javascript
import React, { useState, useEffect } from 'react';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { useNavigate } from 'react-router-dom';
import { createItem, getCategories } from '../services/api';

const PostItemSchema = Yup.object({
  title: Yup.string()
    .required('Title is required')
    .min(3, 'Title must be at least 3 characters')
    .max(100, 'Title must be less than 100 characters'),
  description: Yup.string()
    .max(1000, 'Description must be less than 1000 characters'),
  condition: Yup.string()
    .oneOf(['Like New', 'Good', 'Fair', 'Needs Repair'], 'Invalid condition'),
  pickup_location: Yup.string()
    .required('Pickup location is required')
    .max(200, 'Location too long'),
  pickup_days: Yup.string(),
  pickup_times: Yup.string(),
  special_instructions: Yup.string(),
  category_id: Yup.number()
    .required('Category is required')
    .positive('Please select a category'),
  photo_url: Yup.string()
    .url('Must be a valid URL')
});

const PostItemPage = () => {
  const navigate = useNavigate();
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    try {
      const response = await getCategories();
      setCategories(response.data);
    } catch (error) {
      console.error('Failed to fetch categories:', error);
    }
  };

  const formik = useFormik({
    initialValues: {
      title: '',
      description: '',
      condition: 'Good',
      pickup_location: '',
      pickup_days: '',
      pickup_times: '',
      special_instructions: '',
      category_id: '',
      photo_url: ''
    },
    validationSchema: PostItemSchema,
    onSubmit: async (values, { setSubmitting, setErrors }) => {
      try {
        await createItem(values);
        navigate('/');
      } catch (error) {
        setErrors({ general: error.response?.data?.error || 'Failed to post item' });
      }
      setSubmitting(false);
    }
  });

  return (
    <div style={{ maxWidth: '600px', margin: '2rem auto' }}>
      <h2>Post an Item to Give Away</h2>
      
      {formik.errors.general && (
        <div style={{ color: 'red', marginBottom: '1rem' }}>
          {formik.errors.general}
        </div>
      )}
      
      <form onSubmit={formik.handleSubmit}>
        {/* Title */}
        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="title">Title *</label>
          <input
            id="title"
            name="title"
            type="text"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.title}
            style={{ width: '100%', padding: '0.5rem' }}
          />
          {formik.touched.title && formik.errors.title && (
            <div style={{ color: 'red' }}>{formik.errors.title}</div>
          )}
        </div>

        {/* Category */}
        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="category_id">Category *</label>
          <select
            id="category_id"
            name="category_id"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.category_id}
            style={{ width: '100%', padding: '0.5rem' }}
          >
            <option value="">Select a category</option>
            {categories.map(cat => (
              <option key={cat.id} value={cat.id}>{cat.name}</option>
            ))}
          </select>
          {formik.touched.category_id && formik.errors.category_id && (
            <div style={{ color: 'red' }}>{formik.errors.category_id}</div>
          )}
        </div>

        {/* Description */}
        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="description">Description</label>
          <textarea
            id="description"
            name="description"
            rows="4"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.description}
            style={{ width: '100%', padding: '0.5rem' }}
          />
          {formik.touched.description && formik.errors.description && (
            <div style={{ color: 'red' }}>{formik.errors.description}</div>
          )}
        </div>

        {/* Condition */}
        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="condition">Condition</label>
          <select
            id="condition"
            name="condition"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.condition}
            style={{ width: '100%', padding: '0.5rem' }}
          >
            <option value="Like New">Like New</option>
            <option value="Good">Good</option>
            <option value="Fair">Fair</option>
            <option value="Needs Repair">Needs Repair</option>
          </select>
        </div>

        {/* Pickup Location */}
        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="pickup_location">Pickup Location *</label>
          <input
            id="pickup_location"
            name="pickup_location"
            type="text"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.pickup_location}
            style={{ width: '100%', padding: '0.5rem' }}
            placeholder="e.g., Tuskys Roysambu"
          />
          {formik.touched.pickup_location && formik.errors.pickup_location && (
            <div style={{ color: 'red' }}>{formik.errors.pickup_location}</div>
          )}
        </div>

        {/* Pickup Days */}
        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="pickup_days">Available Days</label>
          <input
            id="pickup_days"
            name="pickup_days"
            type="text"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.pickup_days}
            style={{ width: '100%', padding: '0.5rem' }}
            placeholder="e.g., Saturdays 10am-2pm"
          />
        </div>

        {/* Pickup Times */}
        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="pickup_times">Available Times</label>
          <input
            id="pickup_times"
            name="pickup_times"
            type="text"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.pickup_times}
            style={{ width: '100%', padding: '0.5rem' }}
            placeholder="e.g., 10:00 - 14:00"
          />
        </div>

        {/* Photo URL */}
        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="photo_url">Photo URL</label>
          <input
            id="photo_url"
            name="photo_url"
            type="text"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.photo_url}
            style={{ width: '100%', padding: '0.5rem' }}
            placeholder="https://example.com/photo.jpg"
          />
          {formik.touched.photo_url && formik.errors.photo_url && (
            <div style={{ color: 'red' }}>{formik.errors.photo_url}</div>
          )}
        </div>

        {/* Special Instructions */}
        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="special_instructions">Special Instructions</label>
          <textarea
            id="special_instructions"
            name="special_instructions"
            rows="3"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.special_instructions}
            style={{ width: '100%', padding: '0.5rem' }}
            placeholder="e.g., Call when you arrive"
          />
        </div>

        <button
          type="submit"
          disabled={formik.isSubmitting}
          style={{
            width: '100%',
            padding: '0.75rem',
            backgroundColor: '#4CAF50',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          {formik.isSubmitting ? 'Posting...' : 'Post Item'}
        </button>
      </form>
    </div>
  );
};

export default PostItemPage;
Task 5: Create Item Detail Page
File: src/pages/ItemDetailPage.js

javascript
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { getItem, createRequest, deleteItem, markItemAsGiven } from '../services/api';

const ItemDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [item, setItem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [requestMessage, setRequestMessage] = useState('');
  const [showRequestForm, setShowRequestForm] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    fetchItem();
  }, [id]);

  const fetchItem = async () => {
    try {
      const response = await getItem(id);
      setItem(response.data);
    } catch (error) {
      console.error('Failed to fetch item:', error);
      setError('Item not found');
    } finally {
      setLoading(false);
    }
  };

  const handleRequest = async (e) => {
    e.preventDefault();
    try {
      await createRequest(id, requestMessage);
      setSuccess('Request sent successfully!');
      setRequestMessage('');
      setShowRequestForm(false);
      fetchItem(); // Refresh item data
    } catch (error) {
      setError(error.response?.data?.error || 'Failed to send request');
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this item?')) {
      try {
        await deleteItem(id);
        navigate('/');
      } catch (error) {
        setError(error.response?.data?.error || 'Failed to delete item');
      }
    }
  };

  const handleMarkAsGiven = async () => {
    try {
      await markItemAsGiven(id);
      fetchItem(); // Refresh item data
    } catch (error) {
      setError(error.response?.data?.error || 'Failed to mark item as given');
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;
  if (!item) return <div>Item not found</div>;

  const isOwner = user && user.id === item.giver_id;

  return (
    <div style={{ maxWidth: '800px', margin: '2rem auto' }}>
      {success && (
        <div style={{ color: 'green', marginBottom: '1rem' }}>{success}</div>
      )}
      
      {item.photo_url && (
        <img 
          src={item.photo_url} 
          alt={item.title}
          style={{ width: '100%', maxHeight: '400px', objectFit: 'cover' }}
        />
      )}
      
      <h1>{item.title}</h1>
      
      <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem' }}>
        <span style={{
          backgroundColor: item.is_available ? '#4CAF50' : '#f44336',
          color: 'white',
          padding: '0.25rem 0.5rem',
          borderRadius: '4px'
        }}>
          {item.is_available ? 'Available' : 'Given Away'}
        </span>
        <span>Condition: {item.condition}</span>
        <span>Category: {item.category_name}</span>
      </div>

      <p><strong>Description:</strong> {item.description}</p>
      
      <h3>Pickup Details</h3>
      <p><strong>Location:</strong> {item.pickup_location}</p>
      <p><strong>Days:</strong> {item.pickup_days}</p>
      <p><strong>Time:</strong> {item.pickup_times}</p>
      {item.special_instructions && (
        <p><strong>Instructions:</strong> {item.special_instructions}</p>
      )}

      <p><strong>Posted by:</strong> {item.giver_name}</p>

      {isOwner ? (
        <div style={{ marginTop: '2rem' }}>
          <h3>Manage Your Item</h3>
          <button 
            onClick={() => navigate(`/items/${id}/edit`)}
            style={{ marginRight: '1rem', padding: '0.5rem 1rem' }}
          >
            Edit Item
          </button>
          <button 
            onClick={handleDelete}
            style={{ marginRight: '1rem', padding: '0.5rem 1rem', backgroundColor: '#f44336', color: 'white' }}
          >
            Delete Item
          </button>
          {item.is_available && (
            <button 
              onClick={handleMarkAsGiven}
              style={{ padding: '0.5rem 1rem', backgroundColor: '#FF9800', color: 'white' }}
            >
              Mark as Given
            </button>
          )}
        </div>
      ) : user && item.is_available ? (
        <div style={{ marginTop: '2rem' }}>
          {!showRequestForm ? (
            <button 
              onClick={() => setShowRequestForm(true)}
              style={{ padding: '0.75rem 1.5rem', backgroundColor: '#4CAF50', color: 'white' }}
            >
              Request This Item
            </button>
          ) : (
            <form onSubmit={handleRequest}>
              <h3>Request Item</h3>
              <p>Explain why you need this item:</p>
              <textarea
                value={requestMessage}
                onChange={(e) => setRequestMessage(e.target.value)}
                rows="4"
                style={{ width: '100%', padding: '0.5rem', marginBottom: '1rem' }}
                placeholder="e.g., I'm a student and need this for my hostel..."
                required
                minLength="10"
              />
              <div>
                <button 
                  type="submit"
                  style={{ padding: '0.5rem 1rem', marginRight: '1rem' }}
                >
                  Send Request
                </button>
                <button 
                  type="button"
                  onClick={() => setShowRequestForm(false)}
                  style={{ padding: '0.5rem 1rem' }}
                >
                  Cancel
                </button>
              </div>
            </form>
          )}
        </div>
      ) : !user ? (
        <p>Please <a href="/login">login</a> to request this item.</p>
      ) : null}
    </div>
  );
};

export default ItemDetailPage;
6. GITHUB WORKFLOW
Branch Structure
text
main (production-ready)
├── dev (development branch)
    ├── feature/backend-pagination (Team Member 2)
    ├── feature/backend-validation (Team Member 2)
    ├── feature/frontend-auth (Team Member 3)
    ├── feature/frontend-home (Team Member 3)
    ├── feature/frontend-forms (Team Member 4)
    └── feature/frontend-requests (Team Member 4)