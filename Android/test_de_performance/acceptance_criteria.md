# Acceptance Criteria — Test de performance

Format: Given ... When ... Then ...

## Acceptance Criteria 1: Main Screen Render Time

Given a low-end device on 3G network
When the user opens the main screen
Then first meaningful paint occurs within 2 seconds (p95 < 1.5s)

---

## Acceptance Criteria 2: Background Sync Retry

Given the device is on a slow/unstable network
When a sync operation fails
Then the app retries with exponential backoff (1s, 2s, 4s) without blocking the UI

---

## Acceptance Criteria 3: API Response Latency

Given the app under normal user load
When a search query is submitted
Then the API responds within 300ms (p95)

---
