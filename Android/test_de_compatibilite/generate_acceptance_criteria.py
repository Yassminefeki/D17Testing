#!/usr/bin/env python3
"""Generate acceptance criteria for compatibility tests."""

ACCEPTANCE_CRITERIA = """# Acceptance Criteria — Test de compatibilité

Format: Given ... When ... Then ...

## Acceptance Criteria 1: Android Version Support

Given a device running Android 10, 11, or 12
When the user launches the app
Then the app runs without errors and all features function correctly

---

## Acceptance Criteria 2: Screen Density and Orientation

Given a device with various screen densities and rotated orientation
When the user changes device orientation or runs on different screen densities
Then no UI elements overlap and layouts adapt properly

---

## Acceptance Criteria 3: Tablet Support

Given a tablet with large screen (7+ inches)
When the user launches the app
Then UI elements scale appropriately and features are fully usable

---
"""

if __name__ == "__main__":
    with open("acceptance_criteria.md", "w", encoding="utf-8") as f:
        f.write(ACCEPTANCE_CRITERIA)
    print("✓ Generated acceptance_criteria.md for test_de_compatibilite")
