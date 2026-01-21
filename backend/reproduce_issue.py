import requests
import sys
import uuid

BASE_URL = "http://localhost:8000"

def test_auth_flow():
    # 1. Register a new user
    email = f"test_{uuid.uuid4()}@example.com"
    password = "password123"
    
    print(f"Registering user: {email}")
    try:
        resp = requests.post(f"{BASE_URL}/api/auth/register", json={
            "email": email,
            "password": password
        })
    except Exception as e:
        print(f"Failed to connect to backend: {e}")
        return

    if resp.status_code != 201:
        print(f"Registration failed: {resp.status_code} {resp.text}")
        # Try login if user already exists (though uuid should prevent this)
        resp = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": email,
            "password": password
        })
        if resp.status_code != 200:
            print(f"Login failed: {resp.status_code} {resp.text}")
            return
            
    data = resp.json()
    token = data["access_token"]
    print(f"Got token: {token[:20]}...")

    # 2. Try to access tasks
    headers = {"Authorization": f"Bearer {token}"}
    print("Requesting /api/tasks...")
    resp = requests.get(f"{BASE_URL}/api/tasks", headers=headers)
    
    if resp.status_code == 200:
        print("SUCCESS: Accessed tasks.")
    else:
        print(f"FAILURE: {resp.status_code} {resp.text}")

if __name__ == "__main__":
    test_auth_flow()
