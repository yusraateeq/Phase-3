
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_API_BASE")
MODEL = os.getenv("OPENAI_MODEL")

print(f"Testing Key: {API_KEY[:5]}...")
print(f"Base URL: {BASE_URL}")
print(f"Model: {MODEL}")

# Construct full URL
# Handle potential double slash if BASE_URL ends with /
if BASE_URL.endswith('/'):
    url = f"{BASE_URL}chat/completions"
else:
    url = f"{BASE_URL}/chat/completions"

print(f"Full URL: {url}")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

data = {
    "model": MODEL,
    "messages": [
        {"role": "user", "content": "Hello"}
    ]
}

try:
    response = requests.post(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
