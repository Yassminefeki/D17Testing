# Acceptance Criteria — Test d'intégration

Format: Given ... When ... Then ...

## Acceptance Criteria 1: Profile Persistence Across Devices

Given the user is authenticated and the profile service is available
When the user updates their display name and saves
Then the backend returns 200 and the updated name is returned by the profile endpoint

---

## Acceptance Criteria 2: Concurrent Update Consistency

Given concurrent updates to the same resource from multiple clients
When both clients submit update requests
Then one update succeeds, the other receives a conflict response with the latest state

---

## Acceptance Criteria 3: Auth Service Fallback

Given the external authentication service is unavailable
When a user attempts to log in
Then login fails gracefully with a clear error message, not a crash

---
