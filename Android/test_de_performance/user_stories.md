# User Stories — Test de performance

Format requis:

- En tant que ... I want ... so that ...

Exemples (2–3 user stories pour démarrer):

1) En tant que utilisateur mobile, I want the main screen to render within 2 seconds so that I can start using the app quickly.

2) En tant que utilisateur sur réseau lent, I want background sync to retry with exponential backoff so that data consistency is preserved without blocking the UI.

3) En tant que produit, I want API responses for search to have p95 < 300ms under normal load so that the UX is responsive.

Précisions:
- Définissez métriques (p95, p99, temps moyen) et conditions de test (réseau 3G/4G/Wi-Fi, appareil low-end).

