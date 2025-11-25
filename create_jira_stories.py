import os
import sys
try:
    import requests
except ImportError:
    print("Missing dependency 'requests'. Install with 'pip install -r requirements.txt'.")
    sys.exit(1)
import json
try:
    from dotenv import load_dotenv
except ImportError:
    print("Missing dependency 'python-dotenv'. Install with 'pip install -r requirements.txt'.")
    sys.exit(1)
from urllib.parse import urlparse

# Load environment variables from .env file
load_dotenv()

# --- Configuration from .env file ---
JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
PROJECT_KEY = os.getenv("PROJECT_KEY")
EPIC_KEY = os.getenv("EPIC_KEY")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

# --- Validation ---
missing_vars = []
if not JIRA_DOMAIN or JIRA_DOMAIN == "your-domain.atlassian.net": missing_vars.append("JIRA_DOMAIN")
if not PROJECT_KEY or PROJECT_KEY == "YOUR_PROJECT_KEY": missing_vars.append("PROJECT_KEY")
if not EPIC_KEY or EPIC_KEY == "YOUR_EPIC_KEY": missing_vars.append("EPIC_KEY")
if not JIRA_EMAIL or JIRA_EMAIL == "your-email@example.com": missing_vars.append("JIRA_EMAIL")
if not JIRA_API_TOKEN or JIRA_API_TOKEN == "your-jira-api-token": missing_vars.append("JIRA_API_TOKEN")

if missing_vars:
    print("Error: Please update the following variables in your .env file:")
    for var in missing_vars:
        print(f" - {var}")
    sys.exit(1)

def _normalize_domain(domain: str) -> str:
    """Return a domain/host without scheme or trailing slashes.

    Accepts values like `your-domain.atlassian.net` or
    `https://your-domain.atlassian.net/` and returns `your-domain.atlassian.net`.
    """
    if not domain:
        return domain
    domain = domain.strip()
    parsed = urlparse(domain)
    if parsed.scheme:
        host = parsed.netloc
    else:
        host = domain
    return host.rstrip("/")

API_URL = f"https://{_normalize_domain(JIRA_DOMAIN)}/rest/api/3/issue"
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}
AUTH = (JIRA_EMAIL, JIRA_API_TOKEN)

STORIES_TO_CREATE = [
    {
        "summary": "Test case generation with LLM",
        "description": "Create system that generates test cases using LLM for D17 app"
    },
    {
        "summary": "Automation framework setup",
        "description": "Create the test automation framework (API/UI)"
    },
    {
        "summary": "API & UI test development",
        "description": "Implement tests for all D17 features"
    },
    {
        "summary": "CI/CD integration",
        "description": "Create automated pipelines for running tests"
    },
    {
        "summary": "Reporting & dashboards",
        "description": "Create Allure, Jira dashboards, logs"
    }
]

def create_jira_story(story_data):
    payload = json.dumps({
        "fields": {
            "project": {
                "key": PROJECT_KEY
            },
            "summary": story_data["summary"],
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "text": story_data["description"],
                                "type": "text"
                            }
                        ]
                    }
                ]
            },
            "issuetype": {
                "name": "Story"
            },
            "parent": {
                "key": EPIC_KEY
            }
        }
    })

    print(f"Creating story: '{story_data['summary']}'...")
    response = requests.post(API_URL, headers=HEADERS, auth=AUTH, data=payload)

    if response.status_code == 201:
        issue_key = response.json().get("key")
        print(f"Successfully created story: {story_data['summary']} (Key: {issue_key})")
    else:
        print(f"Failed to create story: {story_data['summary']}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    for story in STORIES_TO_CREATE:
        create_jira_story(story)
