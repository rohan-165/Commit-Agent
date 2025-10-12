import os
import subprocess
import sys
import requests
import json

# Available commit types
COMMIT_TYPES = {
    "1": "FEAT",
    "2": "CHORE",
    "3": "BUG",
    "4": "REFACTOR",
    "5": "FIX",
    "6": "DOCS",
    "7": "TEST",
    "8": "STYLE",
    "9": "PERF"
}

def choose_commit_type():
    print("\nSelect commit type:")
    for key, value in COMMIT_TYPES.items():
        print(f"{key}. {value}")

    choice = input("\nEnter the number corresponding to commit type: ").strip()

    if choice not in COMMIT_TYPES:
        print("❌ Invalid selection. Please run again and choose a valid option.")
        sys.exit(1)

    return COMMIT_TYPES[choice]

def main():
    print("🚀 Starting Commit Agent...\n")

    # 0. Stage all changes automatically
    subprocess.run(["git", "add", "."])
    print("✅ All changes staged.")

    # 1. Get staged changes
    result = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True)
    diff = result.stdout.strip()

    if not diff:
        print("❌ No staged changes found after 'git add .'.")
        sys.exit(1)

    # 2. Choose commit type interactively
    commit_type = choose_commit_type()

    # 3. Optional user note
    user_comment = input("\n📝 Optional note (press Enter to skip): ").strip()

    # 4. Load API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Missing OPENAI_API_KEY environment variable.")
        sys.exit(1)

    # 5. Prepare OpenAI request
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are a professional Git commit assistant.
Analyze the following git diff and generate a concise commit message.
Commit type is: {commit_type}.
User extra note: {user_comment}

Diff:
{diff}
"""

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that writes clean git commit messages."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            data=json.dumps(data)
        )
    except Exception as e:
        print("❌ Failed to call OpenAI API:", e)
        sys.exit(1)

    # 6. Parse response safely
    try:
        response_json = response.json()
    except Exception as e:
        print("❌ Failed to parse API response as JSON:", e)
        print("Raw response:", response.text)
        sys.exit(1)

    if "error" in response_json:
        print("❌ API Error:", response_json["error"]["message"])
        sys.exit(1)

    if "choices" not in response_json or len(response_json["choices"]) == 0:
        print("❌ Unexpected API response, 'choices' missing or empty:", response_json)
        sys.exit(1)

    ai_message = response_json["choices"][0]["message"]["content"].strip()
    final_commit = f"[{commit_type}] {ai_message}"

    # 7. Confirm before committing
    print(f"\n🧠 Suggested commit message:\n{final_commit}")
    confirm = input("\nDo you want to proceed with this commit? (y/n): ").strip().lower()
    if confirm != "y":
        print("🚫 Commit cancelled.")
        sys.exit(0)

    # 8. Run git commit
    subprocess.run(["git", "commit", "-m", final_commit])
    print(f"✅ Commit created:\n{final_commit}")

    # 9. Push to origin
    subprocess.run(["git", "push", "origin", "HEAD"])
    print("🚀 Changes pushed successfully!")

if __name__ == "__main__":
    main()
