import asyncio
import httpx
import os
import sys

async def test_delete_all():
    url = "http://localhost:8000/api/chat"
    # Use the token from previous session
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxYzNkMGM2Mi1mM2UwLTQ1ODMtYjI2Ny0yMGZjODEzYjBkYWQiLCJleHAiOjE3NjkxNjczMzR9.Z7JD_z6KyK4mLlhAK2F4hBC4ISjIUU_FxfL4KkzpGkc"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # First add a few tasks to ensure there's something to delete
    print("Step 1: Adding sample tasks...")
    for i in range(3):
        payload = {"message": f"Add task {i+1}"}
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(url, json=payload, headers=headers)
            print(f"Added task {i+1}: {resp.status_code}")

    # Now request to delete all
    print("\nStep 2: Requesting to delete all tasks...")
    payload = {"message": "Delete all my tasks"}
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(url, json=payload, headers=headers)
        print(f"Status Code: {resp.status_code}")
        if resp.status_code == 200:
            print(f"Response: {resp.json().get('message')}")
        else:
            print(f"Error: {resp.text}")

if __name__ == "__main__":
    asyncio.run(test_delete_all())
