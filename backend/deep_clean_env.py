import re
import os

env_path = '/home/yusraa/Phase-3/Phase-3/backend/.env'

if not os.path.exists(env_path):
    print(f"Error: {env_path} not found")
    exit(1)

with open(env_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Regular expression to find likely key=value pairs, even in a mess
# We look for alphanumeric strings followed by = and then anything until a newline or another likely key starts.
patterns = [
    r'DATABASE_URL=[\w\d:/.@%?&=-]+',
    r'JWT_SECRET=[\w\d]+',
    r'JWT_ALGORITHM=[\w\d]+',
    r'JWT_EXPIRATION_HOURS=[\d]+',
    r'CORS_ORIGINS=[\w\d:/.,-]+',
    r'OPENAI_API_KEY=[\w\d-]+',
    r'OPENAI_API_BASE=[\w\d:/.-]+',
    r'OPENAI_MODEL=[\w\d:/.-]+',
    r'OPENAI_MAX_TOKENS=[\d]+',
    r'APP_NAME=[\w\s\d-]+',
    r'APP_VERSION=[\d.]+',
    r'DEBUG=[\w]+',
    r'HOST=[\d.]+',
    r'PORT=[\d]+'
]

kv_pairs = {}

for p in patterns:
    match = re.search(p, content)
    if match:
        line = match.group(0)
        key, val = line.split('=', 1)
        # Final cleanup for specific keys
        if key == 'JWT_ALGORITHM': val = 'HS256'
        if key == 'JWT_EXPIRATION_HOURS': val = '24'
        if key == 'OPENAI_MAX_TOKENS': val = '512'
        if key == 'OPENAI_API_BASE' and 'openrouter' not in val: val = 'https://openrouter.ai/api/v1'
        
        kv_pairs[key] = val

# Defaults if missing
defaults = {
    'JWT_ALGORITHM': 'HS256',
    'JWT_EXPIRATION_HOURS': '24',
    'OPENAI_MAX_TOKENS': '512',
    'OPENAI_API_BASE': 'https://openrouter.ai/api/v1',
    'CORS_ORIGINS': 'http://localhost:3000,http://127.0.0.1:3000',
    'APP_NAME': 'Todo Backend API',
    'APP_VERSION': '1.0.0',
    'DEBUG': 'True',
    'HOST': '0.0.0.0',
    'PORT': '8000'
}

for k, v in defaults.items():
    if k not in kv_pairs:
        kv_pairs[k] = v

# Reconstruct cleanly
output_lines = [
    "# Database Configuration",
    f"DATABASE_URL={kv_pairs.get('DATABASE_URL', '')}",
    "\n# JWT Configuration",
    f"JWT_SECRET={kv_pairs.get('JWT_SECRET', '6955d19033eca94a674c9cf8cbf4defa5')}",
    f"JWT_ALGORITHM={kv_pairs.get('JWT_ALGORITHM')}",
    f"JWT_EXPIRATION_HOURS={kv_pairs.get('JWT_EXPIRATION_HOURS')}",
    "\n# CORS Configuration",
    f"CORS_ORIGINS={kv_pairs.get('CORS_ORIGINS')}",
    "\n# OpenAI Configuration",
    f"OPENAI_API_KEY={kv_pairs.get('OPENAI_API_KEY', '')}",
    f"OPENAI_API_BASE={kv_pairs.get('OPENAI_API_BASE')}",
    f"OPENAI_MODEL={kv_pairs.get('OPENAI_MODEL', 'google/gemini-2.0-flash-exp:free')}",
    f"OPENAI_MAX_TOKENS={kv_pairs.get('OPENAI_MAX_TOKENS')}",
    "\n# Application Settings",
    f"APP_NAME={kv_pairs.get('APP_NAME')}",
    f"APP_VERSION={kv_pairs.get('APP_VERSION')}",
    f"DEBUG={kv_pairs.get('DEBUG')}",
    "\n# Server Configuration",
    f"HOST={kv_pairs.get('HOST')}",
    f"PORT={kv_pairs.get('PORT')}"
]

with open(env_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines) + '\n')

print("DEEP CLEAN COMPLETE.")
for k in kv_pairs:
    if 'KEY' in k or 'URL' in k or 'SECRET' in k:
        print(f"{k}=***")
    else:
        print(f"{k}={kv_pairs[k]}")
