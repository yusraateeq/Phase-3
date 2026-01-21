import sys
sys.path.insert(0, 'src')
from core.config import settings

print(f"OPENAI_API_BASE: {settings.OPENAI_API_BASE}")
print(f"OPENAI_MODEL: {settings.OPENAI_MODEL}")
