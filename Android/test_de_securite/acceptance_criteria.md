# Acceptance Criteria — Test de sécurité

Format: Given ... When ... Then ...

## Acceptance Criteria 1: Multi-factor Authentication

Given a user with valid credentials and MFA enabled
When the user attempts to log in and provides the second-factor code
Then the user is granted access and a login event is recorded in the audit log

---

## Acceptance Criteria 2: Password Complexity Policy

Given a user creating a new password
When the user enters a password with 8+ chars, uppercase, lowercase, digit, and symbol
Then the password is accepted and stored securely

---

## Acceptance Criteria 3: Lockout After Failed Attempts

Given a user with 4 failed login attempts
When the user attempts the 5th login
Then the account is locked and an unlock email is sent

---
