#!/usr/bin/env python3
"""
User Story and Acceptance Criteria Manager
Automates parsing, generation, and refinement of user stories and acceptance criteria
across all test folders in Android/.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Configuration
TEST_FOLDERS = [
    "Android/test_de_securite",
    "Android/test_de_performance",
    "Android/test_d_utilisabilite",
    "Android/test_de_compatibilite",
    "Android/test_de_connectivite",
    "Android/test_d_integration",
]

ACCEPTANCE_CRITERIA_TEMPLATES = {
    "test_de_securite": [
        {
            "story": "multi-factor authentication",
            "given": "a user with valid credentials and MFA enabled",
            "when": "the user attempts to log in and provides the second-factor code",
            "then": "the user is granted access and a login event is recorded in the audit log",
        },
        {
            "story": "password complexity policy",
            "given": "a user creating a new password",
            "when": "the user enters a password with 8+ chars, uppercase, lowercase, digit, and symbol",
            "then": "the password is accepted and stored securely",
        },
        {
            "story": "lockout after failed attempts",
            "given": "a user with 4 failed login attempts",
            "when": "the user attempts the 5th login",
            "then": "the account is locked and an unlock email is sent",
        },
    ],
    "test_de_performance": [
        {
            "story": "main screen render time",
            "given": "a low-end device on 3G network",
            "when": "the user opens the main screen",
            "then": "first meaningful paint occurs within 2 seconds (p95 < 1.5s)",
        },
        {
            "story": "background sync retry",
            "given": "the device is on a slow/unstable network",
            "when": "a sync operation fails",
            "then": "the app retries with exponential backoff (1s, 2s, 4s) without blocking the UI",
        },
        {
            "story": "API response latency",
            "given": "the app under normal user load",
            "when": "a search query is submitted",
            "then": "the API responds within 300ms (p95)",
        },
    ],
    "test_d_utilisabilite": [
        {
            "story": "guided onboarding flow",
            "given": "a new user opening the app for the first time",
            "when": "the user follows the onboarding steps",
            "then": "90% of users complete setup within 5 minutes with satisfaction >= 4/5",
        },
        {
            "story": "primary actions reachability",
            "given": "a user on any screen",
            "when": "the user wants to perform a primary action",
            "then": "the action button is reachable within two taps or less",
        },
        {
            "story": "accessibility support",
            "given": "a user with screen reader enabled",
            "when": "the user navigates the app",
            "then": "all interactive elements have proper labels and screen reader support",
        },
    ],
    "test_de_compatibilite": [
        {
            "story": "Android version support",
            "given": "a device running Android 10, 11, or 12",
            "when": "the user launches the app",
            "then": "the app runs without errors and all features function correctly",
        },
        {
            "story": "screen density and orientation",
            "given": "a device with various screen densities and rotated orientation",
            "when": "the user changes device orientation or runs on different screen densities",
            "then": "no UI elements overlap and layouts adapt properly",
        },
        {
            "story": "tablet support",
            "given": "a tablet with large screen (7+ inches)",
            "when": "the user launches the app",
            "then": "UI elements scale appropriately and features are fully usable",
        },
    ],
    "test_de_connectivite": [
        {
            "story": "offline action queueing",
            "given": "the device is offline",
            "when": "the user submits an action (e.g., message, data update)",
            "then": "the action is saved locally and synced when connectivity is restored",
        },
        {
            "story": "offline status indicator",
            "given": "the app is offline or has pending actions",
            "when": "the user looks at the UI",
            "then": "an offline indicator is visible and retry options are available",
        },
        {
            "story": "packet loss resilience",
            "given": "the network experiences intermittent packet loss",
            "when": "a network request is made",
            "then": "the app retries gracefully and preserves data integrity",
        },
    ],
    "test_d_integration": [
        {
            "story": "profile persistence across devices",
            "given": "the user is authenticated and the profile service is available",
            "when": "the user updates their display name and saves",
            "then": "the backend returns 200 and the updated name is returned by the profile endpoint",
        },
        {
            "story": "concurrent update consistency",
            "given": "concurrent updates to the same resource from multiple clients",
            "when": "both clients submit update requests",
            "then": "one update succeeds, the other receives a conflict response with the latest state",
        },
        {
            "story": "auth service fallback",
            "given": "the external authentication service is unavailable",
            "when": "a user attempts to log in",
            "then": "login fails gracefully with a clear error message, not a crash",
        },
    ],
}


class UserStoryManager:
    """Manages user stories and acceptance criteria across test folders."""

    def __init__(self, base_path: str = "."):
        self.base_path = base_path

    def parse_user_stories(self, folder: str) -> List[str]:
        """Extract user stories from user_stories.md."""
        file_path = Path(self.base_path) / folder / "user_stories.md"
        if not file_path.exists():
            return []

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract numbered stories (pattern: "N) En tant que ... so that ...")
        stories = re.findall(r"\d+\)\s+(.+?)(?=\n\d+\)|Notes|Précisions|$)", content, re.DOTALL)
        return [story.strip() for story in stories]

    def generate_acceptance_criteria(self, folder: str, story_number: int) -> str:
        """Generate acceptance criteria in Given/When/Then format."""
        test_type = folder.split("/")[-1]
        
        if test_type not in ACCEPTANCE_CRITERIA_TEMPLATES:
            return "# Acceptance Criteria (template not found)\n\nPlease define criteria manually."

        templates = ACCEPTANCE_CRITERIA_TEMPLATES[test_type]
        if story_number > len(templates):
            return "# Acceptance Criteria (out of range)\n\nPlease define criteria manually."

        criteria = templates[story_number - 1]
        return (
            f"**Story**: {criteria['story']}\n\n"
            f"Given {criteria['given']}\n"
            f"When {criteria['when']}\n"
            f"Then {criteria['then']}\n"
        )

    def generate_all_acceptance_criteria(self, folder: str) -> str:
        """Generate all acceptance criteria for a folder."""
        user_stories = self.parse_user_stories(folder)
        if not user_stories:
            return "# Acceptance Criteria — [No user stories found]\n\nPlease add user stories first.\n"

        output = f"# Acceptance Criteria — {folder.split('/')[-1]}\n\n"
        output += "Format: Given ... When ... Then ...\n\n"

        for idx, story in enumerate(user_stories, 1):
            output += f"## Story {idx}\n"
            output += f"{story}\n\n"
            output += self.generate_acceptance_criteria(folder, idx)
            output += "\n---\n\n"

        return output

    def save_acceptance_criteria(self, folder: str) -> bool:
        """Save generated acceptance criteria to file."""
        file_path = Path(self.base_path) / folder / "acceptance_criteria.md"
        criteria = self.generate_all_acceptance_criteria(folder)

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(criteria)
            return True
        except Exception as e:
            print(f"Error saving {file_path}: {e}")
            return False

    def refine_user_story(self, story: str) -> str:
        """Refine a user story for consistency and clarity."""
        # Ensure proper format: "As a ... I want ... so that ..."
        if " I want " not in story and " i want " not in story.lower():
            return f"[NEEDS REFINEMENT] {story}"

        # Normalize capitalization and punctuation
        story = story.strip()
        if not story.endswith("."):
            story += "."

        return story

    def generate_report(self) -> str:
        """Generate a summary report of all user stories and criteria."""
        report = "# User Story and Acceptance Criteria Report\n\n"
        report += "Generated on: 2025-12-03\n\n"

        for folder in TEST_FOLDERS:
            if not (Path(self.base_path) / folder).exists():
                continue

            stories = self.parse_user_stories(folder)
            report += f"## {folder}\n"
            report += f"- Total User Stories: {len(stories)}\n"

            for idx, story in enumerate(stories, 1):
                refined = self.refine_user_story(story)
                report += f"  - **Story {idx}**: {refined[:80]}...\n"

            report += "\n"

        return report


def main():
    """Main execution."""
    manager = UserStoryManager()

    print("=" * 70)
    print("User Story and Acceptance Criteria Manager")
    print("=" * 70)

    # Generate acceptance criteria for all test folders
    print("\nGenerating acceptance criteria...")
    for folder in TEST_FOLDERS:
        folder_path = Path(folder)
        if folder_path.exists():
            if manager.save_acceptance_criteria(folder):
                print(f"✓ Generated criteria for {folder}")
            else:
                print(f"✗ Failed to generate criteria for {folder}")
        else:
            print(f"⊘ Folder not found: {folder}")

    # Print report
    print("\n" + "=" * 70)
    print(manager.generate_report())
    print("=" * 70)

    print("\nNext steps:")
    print("1. Review and refine user stories in each user_stories.md file")
    print("2. Review and customize acceptance criteria in each acceptance_criteria.md file")
    print("3. Create Jira tickets or run automated tests based on the criteria")
    print("4. Re-run this script after making updates to regenerate criteria")


if __name__ == "__main__":
    main()
