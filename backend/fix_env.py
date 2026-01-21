import os

ENV_FILE = ".env"
TARGET_KEY = "OPENAI_API_BASE"
CORRECT_VALUE = "https://openrouter.ai/api/v1"

def fix_env():
    if not os.path.exists(ENV_FILE):
        print(f"Error: {ENV_FILE} not found.")
        return

    with open(ENV_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    found = False
    modified = False

    for line in lines:
        if line.strip().startswith(f"{TARGET_KEY}="):
            current_val = line.split("=", 1)[1].strip()
            if current_val != CORRECT_VALUE:
                print(f"Found incorrect {TARGET_KEY}: {current_val}")
                new_lines.append(f"{TARGET_KEY}={CORRECT_VALUE}\n")
                modified = True
            else:
                print(f"{TARGET_KEY} is already correct.")
                new_lines.append(line)
            found = True
        else:
            new_lines.append(line)

    if not found:
        print(f"{TARGET_KEY} not found. Appending it.")
        new_lines.append(f"\n{TARGET_KEY}={CORRECT_VALUE}\n")
        modified = True

    if modified:
        with open(ENV_FILE, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        print(f"Successfully updated {ENV_FILE}")
    else:
        print("No changes needed.")

if __name__ == "__main__":
    fix_env()
