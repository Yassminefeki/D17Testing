#!/usr/bin/env python3
"""
create_jira_stories.py — Crée des stories Jira prédéfinies pour le projet d'automatisation D17.
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
    print("\n💡 TIP: Assurez-vous que JIRA_DOMAIN, JIRA_EMAIL, JIRA_API_TOKEN sont remplis dans config.py.")
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

# Configuration Jira
API_URL = f"https://{_normalize_domain(Config.JIRA_DOMAIN)}/rest/api/3/issue"
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}
AUTH = (Config.JIRA_EMAIL, Config.JIRA_API_TOKEN)

# --- Stories Adaptées au Projet D17 ---
STORIES_TO_CREATE = [
    {
        "summary": "Génération de Cas de Test via LLM (D17)",
        "description": "Mettre en place la méthodologie et les prompts pour générer automatiquement les cas de test fonctionnels et non-fonctionnels (login, transferts, recharges) de l'application D17, en utilisant un Large Language Model."
    },
    {
        "summary": "Mise en Place du Framework d'Automatisation (Appium/Pytest)",
        "description": "Concevoir et développer l'architecture du framework de tests mobiles avec Python, Appium et Pytest. Inclut la gestion des données de test (JSON) et la configuration des environnements d'exécution (émulateurs)."
    },
    {
        "summary": "Développement des Tests UI Mobile et de Charge (D17)",
        "description": "Implémenter les tests UI (Appium) pour la validation fonctionnelle, ainsi que les scripts de tests de charge (JMeter) pour simuler la concurrence sur les APIs critiques (Connexion, Recharge)."
    },
    {
        "summary": "Intégration et Exécution CI/CD (GitHub Actions)",
        "description": "Créer et configurer les pipelines GitHub Actions pour automatiser l'exécution des tests Appium (mobile) et JMeter (charge), assurant une exécution rapide après chaque intégration de code."
    },
    {
        "summary": "Reporting, Visualisation et Tableaux de Bord",
        "description": "Mettre en place la génération de rapports détaillés (Allure) et intégrer les métriques de test (succès/échec, performance) dans les tableaux de bord Jira pour le suivi du projet et la visibilité."
    }
]

def create_jira_story(story_data: dict) -> bool:
    """Crée une story Jira."""
    # Assurez-vous que l'EPIC_KEY est définie pour lier les stories
    if not Config.EPIC_KEY or Config.EPIC_KEY == "EPIC_KEY_HERE":
        print("❌ ERREUR: Config.EPIC_KEY n'est pas configurée dans config.py.")
        return False
        
    payload = json.dumps({
        "fields": {
            "project": {"key": Config.PROJECT_KEY},
            "summary": story_data["summary"],
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "text": story_data["description"],
                                "type": "text"
                            }
                        ]
                    }
                ]
            },
            "issuetype": {"name": "Story"},
            # Lier toutes les stories à l'épic définie dans config.py
            "parent": {"key": Config.EPIC_KEY} 
        }
    })

    try:
        print(f"  📝 Création: '{story_data['summary']}'...", end=" ")
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
    print("CRÉATION DE STORIES JIRA POUR LE PROJET D17")
    print("=" * 70)
    print(f"\n🎯 Projet: {Config.PROJECT_KEY}")
    print(f"📎 Epic parente: {Config.EPIC_KEY}")
    print(f"🔗 Jira: {Config.JIRA_DOMAIN}")
    print(f"\n📋 {len(STORIES_TO_CREATE)} story(ies) à créer...\n")

    success_count = 0
    fail_count = 0

    for story in STORIES_TO_CREATE:
        if create_jira_story(story):
            success_count += 1
        else:
            fail_count += 1

    print("\n" + "=" * 70)
    print("RÉSUMÉ")
    print("=" * 70)
    print(f"✅ Succès: {success_count}/{len(STORIES_TO_CREATE)}")
    if fail_count > 0:
        print(f"❌ Échecs: {fail_count}/{len(STORIES_TO_CREATE)}")
    print("=" * 70 + "\n")

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())