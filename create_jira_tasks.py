import os
import sys
import json
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration from .env file ---
JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
PROJECT_KEY = os.getenv("PROJECT_KEY")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

# --- Validation (ensure .env is set up) ---
if not all([JIRA_DOMAIN, PROJECT_KEY, JIRA_EMAIL, JIRA_API_TOKEN]):
    print("Error: Please ensure all required variables are set in your .env file.")
    sys.exit(1)

# --- Tasks to Create ---
# IMPORTANT: Ensure the parent_story_key values match your actual Jira Story keys.

TASKS_TO_CREATE = [
    # 4.1 Under Story: “Test case generation with LLM” (DT-2)
    {
        "parent_story_key": "DT-2",
        "summary": "Write prompt structure",
        "description": "Define reusable prompts for generating test cases.",
        "issuetype": "Sous-tâche"
    },
    {
        "parent_story_key": "DT-2",
        "summary": "Generate initial test cases",
        "description": "Use LLM to produce test cases for login, payments, transfers, etc.",
        "issuetype": "Sous-tâche"
    },

    # 4.2 Under Story: “Automation framework setup” (DT-3)
    {
        "parent_story_key": "DT-3",
        "summary": "Choose programming language & framework",
        "description": "Select appropriate language and framework for test automation.",
        "issuetype": "Sous-tâche"
    },
    {
        "parent_story_key": "DT-3",
        "summary": "Project scaffolding setup",
        "description": "Set up the basic project structure and folders.",
        "issuetype": "Sous-tâche"
    },
    {
        "parent_story_key": "DT-3",
        "summary": "Install dependencies",
        "description": "Install all necessary libraries and tools.",
        "issuetype": "Sous-tâche"
    },
    {
        "parent_story_key": "DT-3",
        "summary": "Integrate Gherkin or PyTest-BDD",
        "description": "Integrate BDD frameworks like Gherkin or PyTest-BDD for test definition.",
        "issuetype": "Sous-tâche"
    },

    # 4.3 Under Story: “API & UI test development” (DT-4)
    {
        "parent_story_key": "DT-4",
        "summary": "API tests structure",
        "description": "Define the structure for API test cases.",
        "issuetype": "Sous-tâche"
    },
    {
        "parent_story_key": "DT-4",
        "summary": "UI tests structure",
        "description": "Define the structure for UI test cases.",
        "issuetype": "Sous-tâche"
    },
    {
        "parent_story_key": "DT-4",
        "summary": "Data mocks",
        "description": "Create mock data for testing purposes.",
        "issuetype": "Sous-tâche"
    },
    {
        "parent_story_key": "DT-4",
        "summary": "Document endpoints",
        "description": "Document all API endpoints used in testing.",
        "issuetype": "Sous-tâche"
    },

    # 4.4 Under Story: “CI/CD integration” (DT-5)
    {
        "parent_story_key": "DT-5",
        "summary": "GitHub Actions workflow: build",
        "description": "Set up GitHub Actions for building the project.",
        "issuetype": "Sous-tâche"
    },
    {
        "parent_story_key": "DT-5",
        "summary": "GitHub Actions workflow: run tests",
        "description": "Configure GitHub Actions to run automated tests.",
        "issuetype": "Sous-tâche"
    },
    {
        "parent_story_key": "DT-5",
        "summary": "GitHub Actions: upload report",
        "description": "Set up GitHub Actions to upload test reports.",
        "issuetype": "Sous-tâche"
    },
    {
        "parent_story_key": "DT-5",
        "summary": "GitHub → Jira integration",
        "description": "Integrate GitHub with Jira for seamless updates.",
        "issuetype": "Sous-tâche"
    },

    # 4.5 Under Story: “Reporting & dashboards” (DT-6)
    {
        "parent_story_key": "DT-6",
        "summary": "Install Allure",
        "description": "Install Allure reporting framework.",
        "issuetype": "Sous-tâche"
    },
    {
        "parent_story_key": "DT-6",
        "summary": "Generate reports",
        "description": "Configure and generate test reports.",
        "issuetype": "Sous-tâche"
    },
    {
        "parent_story_key": "DT-6",
        "summary": "Connect Allure → Jira",
        "description": "Integrate Allure reports with Jira dashboards.",
        "issuetype": "Sous-tâche"
    },
    {
        "parent_story_key": "DT-6",
        "summary": "Create Jira Dashboard",
        "description": "Design and create a comprehensive Jira dashboard.",
        "issuetype": "Sous-tâche"
    }
]

# --- Jira API Details ---
API_URL = f"https://{JIRA_DOMAIN}/rest/api/3/issue"
HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}
AUTH = (JIRA_EMAIL, JIRA_API_TOKEN)


def create_jira_issue(task_data):
    """Creates a new issue in Jira."""
    parent_key = task_data.get("parent_story_key")
    if not parent_key or parent_key == "PARENT_STORY_KEY_HERE":
        print(f"Error: You must set 'parent_story_key' for the task '{task_data['summary']}'.")
        print("Please edit the create_jira_tasks.py script.")
        return

    payload = json.dumps({
        "fields": {
            "project": {"key": PROJECT_KEY},
            "parent": {"key": parent_key},
            "summary": task_data["summary"],
            "description": {
                "type": "doc",
                "version": 1,
                "content": [{"type": "paragraph", "content": [{"text": task_data["description"], "type": "text"}]}]
            },
            "issuetype": {"name": task_data["issuetype"]}
        }
    })

    print(f"Creating '{task_data['summary']}' under story {parent_key}...")
    try:
        response = requests.post(API_URL, headers=HEADERS, auth=AUTH, data=payload)
        response.raise_for_status()  # Raises an exception for bad responses (4xx or 5xx)

        issue_key = response.json().get("key")
        print(f"  Successfully created issue: {issue_key}")

    except requests.exceptions.HTTPError as e:
        print(f"  Failed to create issue: {task_data['summary']}")
        print(f"  Status Code: {e.response.status_code}")
        print(f"  Response: {e.response.text}")
    except Exception as e:
        print(f"  An unexpected error occurred: {e}")


if __name__ == "__main__":
    print("Starting Jira task creation...")
    for task in TASKS_TO_CREATE:
        create_jira_issue(task)
    print("Finished.")