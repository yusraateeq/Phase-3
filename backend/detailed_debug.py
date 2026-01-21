import sys
import os
from uuid import UUID
import dotenv

# Add src to python path
sys.path.append(os.path.join(os.getcwd(), 'src'))

# Manually load .env to check what's inside
dotenv.load_dotenv()

print("--- ENV VAR CHECK ---")
print(f"ENV OPENAI_API_BASE: {os.getenv('OPENAI_API_BASE')}")
print(f"ENV OPENAI_MODEL: {os.getenv('OPENAI_MODEL')}")
print(f"ENV OPENAI_API_KEY (prefix): {str(os.getenv('OPENAI_API_KEY'))[:10]}...")

try:
    from core.config import settings
    print("\n--- SETTINGS CHECK ---")
    print(f"SETTINGS OPENAI_API_BASE: {settings.OPENAI_API_BASE}")
    print(f"SETTINGS OPENAI_MODEL: {settings.OPENAI_MODEL}")
    print(f"SETTINGS OPENAI_API_KEY (prefix): {settings.OPENAI_API_KEY[:10]}...")

    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_API_BASE,
        model=settings.OPENAI_MODEL
    )
    
    print("\n--- LLM OBJECT CHECK ---")
    print(f"LLM base_url: {llm.openai_api_base}") # In some versions it's openai_api_base internal attribute
    
    if "openrouter" in str(settings.OPENAI_API_BASE).lower():
        print("\nSUCCESS: Configuration seems correct for OpenRouter.")
    else:
        print("\nFAILURE: Configuration is still pointing to OpenAI default.")
        print("Please ensure your .env file contains: OPENAI_API_BASE=https://openrouter.ai/api/v1")

except Exception as e:
    print(f"\nERROR: {type(e).__name__}: {e}")
