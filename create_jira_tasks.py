#!/usr/bin/env python3
"""
create_jira_tasks.py — Crée des sous-tâches Jira sous les stories pour le projet D17.
Utilise la configuration centralisée depuis config.py.
"""

import sys
try:
    import requests
except ImportError:
    print("❌ ERREUR: Package 'requests' non trouvé.")
    print("   Installez-le: pip install requests")
    sys.exit(1)

import json
from urllib.parse import urlparse

try:
    from config import Config
except ImportError:
    print("❌ ERREUR: config.py non trouvé dans le répertoire courant.")
    sys.exit(1)

# --- Validation ---
if not Config.validate_jira():
    print("\n💡 TIP: Assurez-vous que les valeurs Jira sont remplies dans config.py.")
    sys.exit(1)

def _normalize_domain(domain: str) -> str:
    """Normalise un domaine (supprime schéma et slashes)."""
    if not domain:
        return domain
    domain = domain.strip()
    parsed = urlparse(domain)
    if parsed.scheme:
        host = parsed.netloc
    else:
        host = domain
    return host.rstrip("/")

# --- Tasks to Create (ADAPTATION POUR LE PROJET D17) ---
# IMPORTANT: REMPLACEZ CES CLÉS (DT-X) par les CLÉS RÉELLES des Stories créées par l'autre script.

TASKS_TO_CREATE = [
    # 4.1 Under Story: “Génération de Cas de Test via LLM (D17)” (DT-1)
    {
        "parent_story_key": "D17TES-24", # CLÉ À REMPLACER
        "summary": "Définir la structure des prompts (Connexion, Recharge, Journal)",
        "description": "Créer et valider les prompts réutilisables pour générer les cas de test de base (positifs/négatifs) pour les fonctions clés de D17.",
        "issuetype": "Sous-tâche"
    },
    {
        "parent_story_key": "D17TES-24", # CLÉ À REMPLACER
        "summary": "Générer les cas de test pour les scénarios Négatifs de la Connexion",
        "description": "Utiliser le LLM pour produire un jeu complet de cas de test incluant les règles de longueur de mot de passe, de caractères spéciaux et l'absence de données (cas vide).",
        "issuetype": "Sous-tâche"
    },

    # 4.2 Under Story: “Mise en Place du Framework d'Automatisation (Appium/Pytest)” (DT-2)
    {
        "parent_story_key": "D17TES-25", # CLÉ À REMPLACER
        "summary": "Mise en place de l'environnement Appium/Python",
        "description": "Installer les dépendances Python (`appium-python-client`, `pytest`) et configurer le projet pour l'exécution des tests mobiles.",
        "issuetype": "Sous-tâche"
    },
    {
        "parent_story_key": "D17TES-25", # CLÉ À REMPLACER
        "summary": "Configuration des émulateurs Android et des capacités Appium",
        "description": "Créer et démarrer les AVDs (Android Virtual Devices) nécessaires et s'assurer que les capacités Appium correspondent à l'application D17 (`appPackage`, `appActivity`).",
        "issuetype": "Sous-tâche"
    },
    {
        "parent_story_key": "D17TES-25", # CLÉ À REMPLACER
        "summary": "Implémentation de la lecture des données depuis TestCaseConnect.json",
        "description": "Développer la logique dans le framework pour lire le fichier JSON des cas de test et itérer sur les données pour l'exécution.",
        "issuetype": "Sous-tâche"
    },

    # 4.3 Under Story: “Développement des Tests UI Mobile et de Charge (D17)” (DT-3)
    {
        "parent_story_key": "D17TES-26", # CLÉ À REMPLACER
        "summary": "Capture du trafic API et Corrélation du Token d'Accès",
        "description": "Utiliser Charles/Fiddler pour capturer les requêtes HTTPS de Connexion, identifier le Token d'Accès (JWT) et définir l'extracteur nécessaire pour JMeter.",
        "issuetype": "Sous-tâche"
    },
    {
        "parent_story_key": "D17TES-26", # CLÉ À REMPLACER
        "summary": "Développement du script JMeter pour le scénario de Charge (Connexion + Recharge)",
        "description": "Créer le scénario JMeter pour simuler plusieurs utilisateurs effectuant la séquence de Connexion puis de Recharge mobile, en assurant la corrélation.",
        "issuetype": "Sous-tâche"
    },
    {
        "parent_story_key": "D17TES-26", # CLÉ À REMPLACER
        "summary": "Implémenter les tests de la fonction de Connexion (Validation Inline/Pop-up)",
        "description": "Coder le scénario Appium pour la connexion, incluant la gestion des messages d'erreur (Pop-up VEUILLEZ VÉRIFIER VOS DONNÉES ou erreurs Inline) basés sur les IDs spécifiques de l'application.",
        "issuetype": "Sous-tâche"
    },

    # 4.4 Under Story: “Intégration et Exécution CI/CD (GitHub Actions)” (DT-4)
    {
        "parent_story_key": "D17TES-27", # CLÉ À REMPLACER
        "summary": "Créer le workflow GitHub Actions pour les tests Appium",
        "description": "Mettre en place la CI pour démarrer l'environnement virtuel (émulateur + Appium Server) et exécuter les tests mobiles Pytest/Python.",
        "issuetype": "Sous-tâche"
    },
    {
        "parent_story_key": "D17TES-27", # CLÉ À REMPLACER
        "summary": "Créer le workflow GitHub Actions pour les tests JMeter",
        "description": "Configurer le job de CI pour lancer les tests de charge JMeter et récupérer les rapports de performance (JTL).",
        "issuetype": "Sous-tâche"
    },

    # 4.5 Under Story: “Reporting, Visualisation et Tableaux de Bord” (DT-5)
    {
        "parent_story_key": "D17TES-28", # CLÉ À REMPLACER
        "summary": "Intégration des captures d'écran dans les rapports",
        "description": "S'assurer que le code Appium attache les captures d'écran (en cas de FAIL/BLOCKED) aux données JSON et aux rapports Allure.",
        "issuetype": "Sous-tâche"
    },
    {
        "parent_story_key": "D17TES-28", # CLÉ À REMPLACER
        "summary": "Configuration des rapports Allure pour les tests fonctionnels",
        "description": "Mettre en place la génération et la publication des rapports Allure pour une visualisation claire et ergonomique des résultats des tests mobiles.",
        "issuetype": "Sous-tâche"
    },
    {
        "parent_story_key": "D17TES-28", # CLÉ À REMPLACER
        "summary": "Création du Tableau de Bord Jira de suivi de projet",
        "description": "Concevoir le tableau de bord Jira avec les filtres JQL et les gadgets pertinents pour suivre l'avancement des Stories et le taux de succès/échec des tests automatisés.",
        "issuetype": "Sous-tâche"
    }
]

# --- Jira API Details ---
API_URL = f"https://{_normalize_domain(Config.JIRA_DOMAIN)}/rest/api/3/issue"
HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}
AUTH = (Config.JIRA_EMAIL, Config.JIRA_API_TOKEN)


def create_jira_issue(task_data: dict) -> bool:
    """Crée une sous-tâche Jira."""
    parent_key = task_data.get("parent_story_key")
    if not parent_key:
        print(f"❌ ERREUR: 'parent_story_key' non défini pour '{task_data['summary']}'.")
        print("   Éditez TASKS_TO_CREATE dans ce script.")
        return False

    # Construction du payload JSON pour l'API Jira
    payload = json.dumps({
        "fields": {
            "project": {"key": Config.PROJECT_KEY},
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

    try:
        print(f"  📝 Création '{task_data['summary']}' sous {parent_key}...", end=" ")
        response = requests.post(API_URL, headers=HEADERS, auth=AUTH, data=payload, timeout=30)
        response.raise_for_status()

        issue_key = response.json().get("key")
        print(f"✅ {issue_key}")
        return True

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP {e.response.status_code}")
        print(f"     Réponse: {e.response.text[:200]}")
        return False
    except requests.exceptions.Timeout:
        print(f"❌ Timeout (30s)")
        return False
    except Exception as e:
        print(f"❌ Erreur: {str(e)[:100]}")
        return False


def main():
    """Point d'entrée principal."""
    print("\n" + "=" * 70)
    print("CRÉATION DE SOUS-TÂCHES JIRA POUR LE PROJET D17")
    print("=" * 70)
    print(f"\n🎯 Projet: {Config.PROJECT_KEY}")
    print(f"🔗 Jira Domain: {_normalize_domain(Config.JIRA_DOMAIN)}")
    print(f"\n📋 {len(TASKS_TO_CREATE)} sous-tâche(s) à créer...")

    success_count = 0
    fail_count = 0

    current_parent = None
    for task in TASKS_TO_CREATE:
        if task["parent_story_key"] != current_parent:
            current_parent = task["parent_story_key"]
            print(f"\n--- Sous-tâches pour Story: {current_parent} ---")

        if create_jira_issue(task):
            success_count += 1
        else:
            fail_count += 1

    print("\n" + "=" * 70)
    print("RÉSUMÉ FINAL")
    print("=" * 70)
    print(f"✅ Succès: {success_count}/{len(TASKS_TO_CREATE)}")
    if fail_count > 0:
        print(f"❌ Échecs: {fail_count}/{len(TASKS_TO_CREATE)}")
    print("=" * 70 + "\n")

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())