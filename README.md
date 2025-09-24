# Commit Agent

A smart Git Commit Agent that analyzes your staged changes and automatically generates a professional commit message using OpenAI.  
It can commit and push your changes in one step, saving time and ensuring consistent commit messages.

---

## Features

- Automatically stages all changes (`git add .`)
- Analyzes the diff of staged files
- Generates concise, context-aware commit messages using OpenAI
- Supports commit types: FEAT, FIX, BUG, REFACTOR, DOCS, CHORE, HOTFIX
- Commits and pushes to the current branch automatically
- Optional user notes can be added to the commit message

---

## Requirements

- Python 3.12+  
- Git installed and configured  
- OpenAI API key  

---

## Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd commit-agent
```
2. **Create a virtual environment (recommended)**
```bash
python3 -m venv venv
source venv/bin/activate
```
3. **Install dependencies**
```bash
pip install requests
```
4. **Set your OpenAI API key**
```bash
export OPENAI_API_KEY="sk-your_openai_api_key_here"
```
Note: Never commit your API key to the repository.

---

## Usage

1. **Stage your changes (optional, the script also stages automatically):**
```bash
git add .
```
2. **Run the commit agent:**
```bash
python3 commit_agent.py <commit_type> "Optional note for the commit"
```

## Examples

```bash
python3 commit_agent.py feature "Add login form with validation"
python3 commit_agent.py fix "Resolve crash when loading user profile"
python3 commit_agent.py chore "Update dependencies and clean code"
```

---

## Benefits

 - Saves time writing commit messages
 - Ensures consistent and professional commit format
 - Helps teams maintain readable and descriptive Git history
 - Integrates AI assistance into your development workflow

---

## Optional: Zsh alias

To run the agent from anywhere without typing the full Python command, add this alias to your ~/.zshrc:
```bash
alias commit-agent="python3 /path/to/commit-agent/commit_agent.py"
```
Reload your zsh config:
```bash
source ~/.zshrc
```
Now you can run:
```bash
commit-agent feature "Add search functionality"
```

---

## License

MIT License. Free to use and modify.




