import os
import requests
import json

# --- Configuration ---
JIRA_DOMAIN = "yesminefk.atlassian.net"  # Your Jira domain
PROJECT_KEY = "DT"                      # Your Jira project key
EPIC_KEY = "D17-EP1"                    # The key of your 'D17 Test Automation Project' Epic

# Get credentials from environment variables for security
JIRA_EMAIL = os.environ.get("JIRA_EMAIL")
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN")

if not JIRA_EMAIL or not JIRA_API_TOKEN:
    print("Error: Please set JIRA_EMAIL and JIRA_API_TOKEN environment variables.")
    print("Example: $env:JIRA_EMAIL='your-email@example.com' (PowerShell)")
    print("Example: $env:JIRA_API_TOKEN='your-api-token' (PowerShell)")
    exit(1)

API_URL = f"https://{JIRA_DOMAIN}/rest/api/3/issue"
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
