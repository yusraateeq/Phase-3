import requests
import uuid

BASE_URL = "http://localhost:8000"

def get_token():
    # randomized email to ensure new user
    email = f"dev_{uuid.uuid4().hex[:8]}@example.com" 
    password = "password123"
    
    # Register
    try:
        resp = requests.post(f"{BASE_URL}/api/auth/register", json={
            "email": email,
            "password": password
        })
        if resp.status_code == 201:
            token = resp.json()["access_token"]
            print(f"\n--- COPY THIS TOKEN BELOW ---\n")
            print(token)
            print(f"\n-----------------------------\n")
            print(f"Created temp user: {email} / {password}")
            return
    except:
        pass

    # Fallback to Login
    resp = requests.post(f"{BASE_URL}/api/auth/login", json={
        "email": email,
        "password": password
    })
    
    if resp.status_code == 200:
        token = resp.json()["access_token"]
        print(f"\n--- COPY THIS TOKEN BELOW ---\n")
        print(token)
        print(f"\n-----------------------------\n")
    else:
        print("Failed to get token.")

if __name__ == "__main__":
    get_token()
