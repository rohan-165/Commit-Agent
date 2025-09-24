import os
import subprocess
import sys
import requests
import json

def main():
    if len(sys.argv) < 2:
        print("Usage: python commit_agent.py <commit_type> [optional_comment]")
        print("Example: python commit_agent.py feature 'Add login form'")
        sys.exit(1)

    commit_type = sys.argv[1].upper()  # FEATURE, HOTFIX, BUG, etc.
    user_comment = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""

    # 1. Get staged changes
    result = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True)
    diff = result.stdout.strip()

    if not diff:
        print("❌ No staged changes. Use 'git add .' before running this.")
        sys.exit(1)

    # 2. Load API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Missing OPENAI_API_KEY environment variable.")
        sys.exit(1)

    # 3. Call OpenAI API
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

    response = requests.post("https://api.openai.com/v1/chat/completions",
                             headers=headers, data=json.dumps(data))
    response_json = response.json()

    ai_message = response_json["choices"][0]["message"]["content"].strip()
    final_commit = f"{commit_type}: {ai_message}"

    # 4. Run git commit
    subprocess.run(["git", "commit", "-m", final_commit])
    print(f"✅ Commit created:\n{final_commit}")

    # 5. Push to origin
    subprocess.run(["git", "push", "origin", "HEAD"])

if __name__ == "__main__":
    main()
