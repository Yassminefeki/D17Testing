# Acceptance Criteria — Test de connectivité

Format: Given ... When ... Then ...

## Acceptance Criteria 1: Offline Action Queueing

Given the device is offline
When the user submits an action (e.g., message, data update)
Then the action is saved locally and synced when connectivity is restored

---

## Acceptance Criteria 2: Offline Status Indicator

Given the app is offline or has pending actions
When the user looks at the UI
Then an offline indicator is visible and retry options are available

---

## Acceptance Criteria 3: Packet Loss Resilience

Given the network experiences intermittent packet loss
When a network request is made
Then the app retries gracefully and preserves data integrity

---
