# Android Test Suite — Setup & Usage Guide

## Structure

The workspace contains 6 test folders, each focusing on a specific quality dimension:

```
Android/
├── test_de_securite/
│   ├── README.md
│   ├── user_stories.md
│   ├── acceptance_criteria.md
│   └── generate_acceptance_criteria.py
├── test_de_performance/
│   ├── README.md
│   ├── user_stories.md
│   ├── acceptance_criteria.md
│   └── generate_acceptance_criteria.py
├── test_d_utilisabilite/
│   ├── README.md
│   ├── user_stories.md
│   ├── acceptance_criteria.md
│   └── generate_acceptance_criteria.py
├── test_de_compatibilite/
│   ├── README.md
│   ├── user_stories.md
│   ├── acceptance_criteria.md
│   └── generate_acceptance_criteria.py
├── test_de_connectivite/
│   ├── README.md
│   ├── user_stories.md
│   ├── acceptance_criteria.md
│   └── generate_acceptance_criteria.py
└── test_d_integration/
    ├── README.md
    ├── user_stories.md
    ├── acceptance_criteria.md
    └── generate_acceptance_criteria.py
```

## Files Overview

### `README.md`
- High-level objective for the test folder
- File structure and quick links
- Instructions for use

### `user_stories.md`
- User stories in format: **"As a ... I want ... so that ..."**
- 2–3 example stories per folder (you can add more)
- Tips for refinement

### `acceptance_criteria.md`
- Pre-generated acceptance criteria in **Given/When/Then** format
- One criterion per user story
- Customizable for your specific needs

### `generate_acceptance_criteria.py`
- Standalone script to regenerate criteria (optional)
- Useful if you update user stories

## Quick Start

### 1. Review the Test Structure
```bash
# List all test folders and their files
ls -R Android/
```

### 2. Read & Understand User Stories
Open each `Android/test_*/user_stories.md` and:
- Review the 2–3 example stories
- Add your own stories following the same format
- Refine wording as needed

### 3. Review Acceptance Criteria
Open each `Android/test_*/acceptance_criteria.md` and:
- Verify Given/When/Then format
- Adjust metrics, thresholds, and timelines
- Add more criteria if needed

### 4. Customize for Your Project
- Edit stories: Add project-specific details, roles, contexts
- Edit criteria: Match your infrastructure, devices, performance targets
- Add test data, mocks, fixtures

### 5. Create Jira Tickets (Example)
For each user story, create a Jira ticket with:
- **Summary**: The user story text
- **Description**: Context and links to criteria
- **Acceptance Criteria**: Copy the Given/When/Then items
- **Labels**: `test_de_securite`, `test_de_performance`, etc.

### 6. Implement Tests
Create test files (e.g., `test_security_mfa.py`) in each folder:
```python
# Example: test_security_mfa.py
import pytest

def test_mfa_login_success():
    """Given a user with valid credentials and MFA enabled..."""
    # Setup: create test user with MFA
    # Execute: submit login + MFA code
    # Assert: user logged in, audit log recorded
    pass

def test_mfa_login_invalid_code():
    """Given invalid MFA code..."""
    # Setup, Execute, Assert
    pass
```

## File Format Reference

### User Story Format
```
N) As a <role>, I want <feature> so that <benefit>.

Additional context:
- Preconditions
- Edge cases
- Metrics/SLAs
```

### Acceptance Criteria Format
```
## Acceptance Criteria N: <short title>

Given <precondition(s)>
When <action>
Then <expected result>
```

## Regenerating Criteria (Optional)

If you update user stories, regenerate criteria:
```bash
# Individual folder
cd Android/test_de_securite
python generate_acceptance_criteria.py

# Or run the master script (if available)
python ../../generate_all_criteria.py
```

## Examples

### Security User Story
```
As a user, I want to enable multi-factor authentication 
so that my account is protected against credential compromise.

Metrics:
- MFA enrollment: > 80% adoption target
- MFA latency: < 5 seconds per attempt
```

### Performance Acceptance Criterion
```
Given a low-end device on 3G network
When the user opens the main screen
Then first meaningful paint occurs within 2 seconds (p95 < 1.5s)
```

### Usability Acceptance Criterion
```
Given a new user opening the app for the first time
When the user follows the onboarding steps
Then 90% of users complete setup within 5 minutes with satisfaction >= 4/5
```

## Best Practices

1. **Keep Stories Independent**: Each story should be deliverable on its own
2. **Make Criteria Testable**: Use measurable outcomes (times, thresholds, counts)
3. **Include Edge Cases**: Negative scenarios, boundary conditions, error handling
4. **Update Regularly**: Refine based on test results and feedback
5. **Track Changes**: Use git to version your stories and criteria

## Links & Resources

- **Jira Integration**: Copy user stories directly to Jira via bulk import
- **Testing Frameworks**: pytest (Python), JUnit (Java), Espresso (Android UI)
- **Performance Tools**: JMeter, Locust, Android Profiler
- **Compatibility**: Android Emulator, Firebase Test Lab, BrowserStack
- **Documentation**: See individual `README.md` in each test folder

## Next Steps

1. [ ] Review all 6 test folders
2. [ ] Customize user stories for your app
3. [ ] Refine acceptance criteria metrics
4. [ ] Create Jira tickets
5. [ ] Implement automated tests
6. [ ] Set up CI/CD pipeline
7. [ ] Monitor and iterate

---

**Last Updated**: 2025-12-03
**Status**: Ready for customization and use
