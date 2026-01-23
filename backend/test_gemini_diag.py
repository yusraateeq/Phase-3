import os
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

async def test_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        api_key = api_key.strip().strip('"').strip("'")
    
    endpoints = [
        "https://generativelanguage.googleapis.com/v1beta/openai/",
        "https://generativelanguage.googleapis.com/v1/openai/"
    ]
    
    models_to_test = [
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-2.0-flash-exp"
    ]
    
    for base_url in endpoints:
        print(f"\n=== Testing Endpoint: {base_url} ===")
        client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        
        print("Attempting to list models...")
        try:
            models = await client.models.list()
            print("Successfully listed models!")
            for m in list(models)[:5]:
                print(f" - {m.id}")
        except Exception as e:
            print(f"Failed to list models: {e}")

        for model in models_to_test:
            print(f"--- Testing model: {model} ---")
            try:
                response = await client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": "Say hello!"}],
                    max_tokens=10
                )
                print(f"Success with {model} on {base_url}! Response: {response.choices[0].message.content}")
                return model, base_url
            except Exception as e:
                print(f"Failed: {e}")
    
    return None

async def test_native_gemini():
    print("\n=== Testing Native Gemini SDK ===")
    try:
        import google.generativeai as genai
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            api_key = api_key.strip().strip('"').strip("'")
        
        genai.configure(api_key=api_key)
        
        print("Listing available models...")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f" - {m.name}")
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Say hello!")
        print(f"Success with Native SDK! Response: {response.text}")
        return True
    except Exception as e:
        print(f"Native SDK failed: {e}")
    return False

if __name__ == "__main__":
    # asyncio.run(test_gemini())
    asyncio.run(test_native_gemini())
