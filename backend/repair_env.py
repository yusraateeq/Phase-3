import os

env_path = '/home/yusraa/Phase-3/Phase-3/backend/.env'

if not os.path.exists(env_path):
    print(f"Error: {env_path} not found")
    exit(1)

with open(env_path, 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    line = line.strip()
    if not line or line.startswith('#'):
        new_lines.append(line)
        continue
    
    if '=' in line:
        key, val = line.split('=', 1)
        # Clean up common mangled keys/values
        if key == 'JWT_ALGORITHM':
            val = 'HS256'
        elif key == 'JWT_EXPIRATION_HOURS':
            val = '24'
        elif key == 'CORS_ORIGINS' and '3eca94a674c9cf8cbf4defa5' in val:
            val = 'http://localhost:3000,http://127.0.0.1:3000'
        elif key == 'DATABASE_URL':
            # Remove junk at the end if present
            if val.endswith('577a6701d25937a7652b8aa9826ed916f8647564afefe'):
                val = val.replace('577a6701d25937a7652b8aa9826ed916f8647564afefe', '')
        
        new_lines.append(f"{key}={val}")

# Ensure OpenRouter settings are there if we missed them in the mangled mess
expected_settings = {
    'OPENAI_API_BASE': 'https://openrouter.ai/api/v1',
    'OPENAI_MAX_TOKENS': '512'
}

keys_present = [l.split('=')[0] for l in new_lines if '=' in l]

for k, v in expected_settings.items():
    if k not in keys_present:
        new_lines.append(f"{k}={v}")

with open(env_path, 'w') as f:
    f.write('\n'.join(new_lines) + '\n')

print("Repair complete. Inspecting cleaned lines:")
for l in new_lines:
    if 'KEY' in l or 'URL' in l or 'SECRET' in l:
        print(f"{l.split('=')[0]}=***")
    else:
        print(l)
