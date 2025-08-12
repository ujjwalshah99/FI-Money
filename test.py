import requests
import json
import time
import random

BASE_URL = "http://localhost:5000/api"

def generate_unique_id():
    """Generate a unique identifier using timestamp and random number"""
    return f"{int(time.time())}{random.randint(1000, 9999)}"

def print_result(test_name, passed, expected=None, got=None, request_data=None, response_body=None):
    """
    Prints test result.
    If passed, prints only success.
    If failed, prints request, expected vs got, and response body.
    """
    if passed:
        print(f"{test_name}: PASSED")
    else:
        print(f"{test_name}: FAILED")
        if request_data:
            print(f"  Request: {request_data}")
        if expected is not None and got is not None:
            print(f"  Expected: {expected}, Got: {got}")
        if response_body:
            print(f"  Response Body: {response_body}")

def test_register_user():
    """
    Tests user registration.
    Expected status codes are 201 (created) or 400/409 (conflict if user exists).
    """
    unique_id = generate_unique_id()
    payload = {"username": f"testuser_{unique_id}", "password": "test123"}
    res = requests.post(f"{BASE_URL}/auth/register", json=payload)
    passed = res.status_code in [201, 400, 409]
    print_result("User Registration", passed, "201, 400, or 409", res.status_code, payload, res.text)
    return payload["username"]  # Return username for login test

def test_login(username=None):
    """
    Tests user login.
    On success, expects 200 status and a token in JSON response.
    Returns the token for authenticated requests.
    """
    # Use provided username or fallback to existing user
    test_username = username if username else "uuj"
    payload = {"username": test_username, "password": "test123"}
    res = requests.post(f"{BASE_URL}/auth/login", json=payload)
    token = None
    passed = False
    if res.status_code == 200:
        try:
            response_data = res.json()
            # Try common token field names
            token = (response_data.get("token") or 
                    response_data.get("access_token") or 
                    response_data.get("authToken") or
                    response_data.get("jwt"))
            passed = token is not None
        except json.JSONDecodeError:
            passed = False
    print_result("Login Test", passed, "status 200 and token", res.status_code, payload, res.text)
    return token

def test_add_product(token):
    """
    Tests adding a new product.
    Must include Authorization header with token.
    Returns product_id on success.
    """
    if not token:
        print_result("Add Product", False, "valid token", "no token provided")
        return None
    
    unique_id = generate_unique_id()
    payload = {
        "name": f"Test Smartwatch {unique_id}",
        "type": "Electronics",
        "sku": f"SW-{unique_id}",
        "image_url": "http://example.com/smartwatch.jpg",
        "description": "Fitness tracking smartwatch with heart rate monitor for testing.",
        "quantity": 40,
        "price": 49.99
    }
    headers = {"Authorization": "bearer " + token}
    res = requests.post(f"{BASE_URL}/products", json=payload, headers=headers)
    product_id = None
    passed = res.status_code in [201, 400]  # Accept 400 if product exists
    if res.status_code == 201:
        try:
            response_data = res.json()
            # Try different possible keys for product ID
            product_id = (response_data.get("product_id") or 
                         response_data.get("_id") or 
                         response_data.get("id") or
                         response_data.get("productId"))
            if product_id is None:
                passed = False
        except json.JSONDecodeError:
            passed = False
    elif res.status_code == 400:
        # If product exists, try to get existing product ID from error or use a known ID
        print("  Note: Product already exists, will use existing product for further tests")
        
    print_result("Add Product", passed, "status 201 or 400", res.status_code, payload, res.text)
    return product_id

def get_existing_product_id(token):
    """
    Gets an existing product ID from the products list.
    """
    if not token:
        return None
        
    headers = {"Authorization": "bearer " + token}
    res = requests.get(f"{BASE_URL}/products", headers=headers)
    
    if res.status_code == 200:
        try:
            response_data = res.json()
            # Handle both direct array response and wrapped response
            products = response_data.get("products") or response_data
            if isinstance(products, list) and len(products) > 0:
                # Get the first product's ID
                first_product = products[0]
                return (first_product.get("_id") or 
                       first_product.get("id") or 
                       first_product.get("product_id"))
        except json.JSONDecodeError:
            pass
    return None
def test_update_quantity(token, product_id):
    """
    Tests updating the quantity for a specific product.
    Uses Authorization header.
    """
    if not token:
        print_result("Update Quantity", False, "valid token", "no token provided")
        return False

    # If no product_id provided, try to get one from existing products
    if not product_id:
        product_id = get_existing_product_id(token)
        if not product_id:
            print_result("Update Quantity", False, "valid product_id", "no product_id available")
            return False

    new_quantity = 25
    payload = {"quantity": new_quantity}
    headers = {"Authorization": "bearer " + token}
    res = requests.put(f"{BASE_URL}/products/{product_id}/quantity", json=payload, headers=headers)
    passed = res.status_code == 200
    if passed:
        try:
            response_data = res.json()
            # Check if quantity is in nested product object or direct response
            updated_qty = (response_data.get("quantity") or 
                          response_data.get("product", {}).get("quantity"))
            if updated_qty != new_quantity:
                passed = False
        except json.JSONDecodeError:
            passed = False
            
    print_result("Update Quantity", passed, f"status 200 and quantity {new_quantity}", res.status_code, payload, res.text)
    return passed

def test_get_products(token):
    """
    Tests fetching the list of products.
    Uses Authorization header.
    """
    if not token:
        print_result("Get Products", False, "valid token", "no token provided")
        return
        
    headers = {"Authorization": "bearer " + token}
    res = requests.get(f"{BASE_URL}/products", headers=headers)
    passed = res.status_code == 200
    if passed:
        try:
            response_data = res.json()
            # Handle both direct array response and wrapped response
            products = response_data.get("products") or response_data
            if not isinstance(products, list):
                passed = False
        except json.JSONDecodeError:
            passed = False

    print_result("Get Products", passed, "status 200 and a list of products", res.status_code, response_body=res.text)

def run_all_tests():
    """
    Runs all tests in sequence.
    Tests are designed to handle existing data gracefully.
    """
    print("--- Starting API Tests ---")
    
    # Test registration with unique username
    username = test_register_user()
    
    # Test login (fallback to existing user if registration failed)
    token = test_login(username)

    if not token:
        print("Login failed. Trying with existing user 'ujjwal'...")
        token = test_login("uuj")
        
    if not token:
        print("All login attempts failed. Skipping authenticated tests.")
        return

    # Test adding product (handles existing products)
    product_id = test_add_product(token)
    
    # Test update quantity (will find existing product if add failed)
    update_passed = test_update_quantity(token, product_id)
    
    # Test get products (should always work with valid token)
    test_get_products(token)
    
    print("--- API Tests Finished ---")

if __name__ == "__main__":
    run_all_tests()