#!/usr/bin/env python
"""
Complete end-to-end test: Register → Login → Chat
"""
import asyncio
import json
import httpx
import sys

BASE_URL = "http://localhost:8000"

async def test_full_flow():
    """Test registration, login, and chat"""
    
    email = "testuser@example.com"
    password = "TestPassword123"
    
    print(f"\n{'='*70}")
    print("END-TO-END API TEST")
    print(f"{'='*70}\n")
    
    async with httpx.AsyncClient(timeout=30) as client:
        # 1. Register
        print("1. Registering test user...")
        try:
            resp = await client.post(
                f"{BASE_URL}/api/auth/register",
                json={"email": email, "password": password}
            )
            print(f"   Status: {resp.status_code}")
            if resp.status_code in [201, 400]:  # 400 if user already exists
                print(f"   ✓ Register successful (or user exists)")
            else:
                print(f"   ✗ Register failed: {resp.text}")
                return False
        except Exception as e:
            print(f"   ✗ Register error: {e}")
            return False
        
        # 2. Login
        print("\n2. Logging in...")
        try:
            resp = await client.post(
                f"{BASE_URL}/api/auth/login",
                json={"email": email, "password": password}
            )
            print(f"   Status: {resp.status_code}")
            if resp.status_code == 200:
                data = resp.json()
                token = data.get("access_token")
                print(f"   ✓ Login successful")
                print(f"   Token: {token[:30]}...")
            else:
                print(f"   ✗ Login failed: {resp.text}")
                return False
        except Exception as e:
            print(f"   ✗ Login error: {e}")
            return False
        
        # 3. Chat
        print("\n3. Testing chat endpoint...")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        try:
            resp = await client.post(
                f"{BASE_URL}/api/chat",
                json={"message": "Hello, can you help me?"},
                headers=headers
            )
            print(f"   Status: {resp.status_code}")
            if resp.status_code == 200:
                data = resp.json()
                message = data.get("message", "")
                print(f"   ✓ Chat endpoint works!")
                print(f"\n   Bot response: {message[:150]}")
                if "error" in message.lower() or "module" in message.lower():
                    print(f"\n   ⚠ WARNING: Response contains error message")
                    print(f"   Full response: {message}")
                    return False
                return True
            else:
                print(f"   ✗ Chat failed: {resp.text}")
                return False
        except Exception as e:
            print(f"   ✗ Chat error: {e}")
            return False

if __name__ == "__main__":
    try:
        success = asyncio.run(test_full_flow())
        if success:
            print(f"\n{'='*70}")
            print("✓ ALL TESTS PASSED!")
            print(f"{'='*70}\n")
            sys.exit(0)
        else:
            print(f"\n{'='*70}")
            print("✗ TESTS FAILED")
            print(f"{'='*70}\n")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nTest cancelled")
        sys.exit(1)
