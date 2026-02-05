
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")
print(f"Testing Key: {API_KEY[:5]}...{API_KEY[-5:] if API_KEY else ''}")

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
headers = {"Content-Type": "application/json"}

try:
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Success! Models available:")
        data = response.json()
        for model in data.get('models', []):
             print(f"- {model['name']}")
    else:
        print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
