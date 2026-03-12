# test_auth.py
import requests
import json

BASE_URL = "http://localhost:5555"

def test_register():
    """Test user registration"""
    print("\n TESTING REGISTRATION...")
    
    # Test valid registration
    valid_user = {
        "phone_number": "0712345678",
        "password": "password123",
        "name": "Test User",
        "location": "Roysambu, Nairobi"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/auth/register",
        json=valid_user
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        print(" Valid registration successful")
        data = response.json()
        print(f"   Token received: {data['token'][:20]}...")
        print(f"   User: {data['user']['name']}")
    else:
        print(f" Failed: {response.text}")
    
    # Test invalid phone number
    invalid_phone = {
        "phone_number": "12345",
        "password": "password123",
        "name": "Test User"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/auth/register",
        json=invalid_phone
    )
    
    print(f"\nTesting invalid phone (12345): {response.status_code}")
    if response.status_code == 400:
        print(" Phone validation working")
    else:
        print(" Phone validation failed")

def test_login():
    """Test user login"""
    print("\n TESTING LOGIN...")
    
    # First create a user
    user_data = {
        "phone_number": "0723456789",
        "password": "testpass123",
        "name": "Login Test User"
    }
    
    requests.post(f"{BASE_URL}/api/auth/register", json=user_data)
    
    # Test valid login
    login_data = {
        "phone_number": "0723456789",
        "password": "testpass123"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json=login_data
    )
    
    print(f"Valid login: {response.status_code}")
    if response.status_code == 200:
        print(" Login successful")
        data = response.json()
        print(f"   Token: {data['token'][:20]}...")
        return data['token']
    else:
        print(f" Login failed: {response.text}")
        return None
    
def test_protected_route(token):
    """Test accessing protected profile route"""
    print("\n TESTING PROTECTED ROUTE...")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{BASE_URL}/api/auth/profile",
        headers=headers
    )
    
    print(f"Profile access: {response.status_code}")
    if response.status_code == 200:
        print(" Protected route accessible")
        print(f"   User profile: {response.json()}")
    else:
        print(f" Protected route failed: {response.text}")

def test_categories():
    """Test category endpoints"""
    print("\n TESTING CATEGORIES...")
    
    # Get all categories
    response = requests.get(f"{BASE_URL}/api/categories/")
    print(f"Get all categories: {response.status_code}")
    if response.status_code == 200:
        categories = response.json()
        print(f" Found {len(categories)} categories")
        for cat in categories[:3]:  # Show first 3
            print(f"   - {cat['name']}: {cat.get('description', '')[:30]}...")

if __name__ == "__main__":
    # FIXED: This was the error - print="="*50 is wrong, should be print("="*50)
    print(" TESTING DECLUTTER254 API")
    print("="*50)
    
    # Run tests
    test_register()
    token = test_login()
    if token:
        test_protected_route(token)
    test_categories()
    
    print("\n" + "="*50)
    print(" TESTS COMPLETE")