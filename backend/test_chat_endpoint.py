#!/usr/bin/env python
"""
Test chat endpoint through actual API call.
"""
import asyncio
import json
import httpx
import os
import sys

async def test_chat_api():
    """Test the /api/chat endpoint"""
    
    # Prepare request
    url = "http://localhost:8000/api/chat"
    payload = {
        "message": "Add a task called 'Buy milk for the party' with high priority",
        "conversation_id": None
    }
    headers = {
        "Content-Type": "application/json",
        # Add auth token if needed
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxYzNkMGM2Mi1mM2UwLTQ1ODMtYjI2Ny0yMGZjODEzYjBkYWQiLCJleHAiOjE3NjkxNjczMzR9.Z7JD_z6KyK4mLlhAK2F4hBC4ISjIUU_FxfL4KkzpGkc"
    }
    
    print(f"\n{'='*70}")
    print("Testing Chat API Endpoint")
    print(f"{'='*70}")
    print(f"URL: {url}")
    print(f"Message: {payload['message']}")
    print(f"{'='*70}\n")
    
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(url, json=payload, headers=headers)
            
            print(f"Status Code: {response.status_code}")
            print(f"Headers: {dict(response.headers)}\n")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Response JSON:")
                print(json.dumps(data, indent=2))
                
                if "message" in data:
                    print(f"\n[OK] SUCCESS! Bot response: {data['message'][:100]}...")
                else:
                    print(f"\n[!] Response received but no 'message' field")
            else:
                print(f"Error Response:")
                print(f"Text: {response.text}")
                print(f"\n[FAIL] FAILED with status {response.status_code}")
                
    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")
        return False
    
    return response.status_code == 200

if __name__ == "__main__":
    try:
        success = asyncio.run(test_chat_api())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nTest cancelled by user")
        sys.exit(1)
