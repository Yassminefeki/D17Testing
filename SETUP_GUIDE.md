# Guide de configuration et usage — D17Testing

## 📋 Table des matières

1. [Configuration initiale](#1-configuration-initiale)
2. [Commandes utiles](#2-commandes-utiles)
3. [Scripts Jira](#3-scripts-jira)
4. [Dépannage](#4-dépannage)

---

## 1. Configuration initiale

### Étape 1 : Installer les dépendances

```bash
python -m pip install -r requirements.txt
```

Packages requis :
- `requests` — pour appels API Jira
- `python-dotenv` — pour charger `.env`
- `pylatex` — pour générer rapports PDF (optionnel)
- `appium-python-client` — pour tests Appium (optionnel)
- `google-genai` — pour génération LLM (optionnel, si GEMINI_API_KEY configurée)

### Étape 2 : Configurer le fichier `.env`

1. Copiez `.env.example` en `.env` :

```bash
copy .env.example .env   # Windows
cp .env.example .env      # Linux/Mac
```

2. Éditez `.env` avec vos valeurs réelles :

```env
# Variables Jira (obligatoires)
JIRA_DOMAIN=your-company.atlassian.net
PROJECT_KEY=DT
EPIC_KEY=DT-1
JIRA_EMAIL=your-email@company.com
JIRA_API_TOKEN=<votre_token_API>

# Variables optionnelles
GEMINI_API_KEY=<votre_clé_genai>
APPIUM_DEVICE_NAME=<votre_device_id>
```

**⚠️ IMPORTANT:** 
- Ne committez JAMAIS `.env` avec vos clés réelles (il est dans `.gitignore`).
- Utilisez `.env.example` comme template pour la documentation.

### Étape 3 : Vérifier la configuration

```bash
python config.py
```

Vous devriez voir ✅ si tout est correct.

---

## 2. Commandes utiles

### Vérifier la configuration

```bash
python config.py
```

### Créer des stories Jira

```bash
python create_jira_stories.py
```

**Sortie attendue :**
```
======================================================================
CRÉATION DE STORIES JIRA
======================================================================

🎯 Projet: DT
📎 Epic: DT-1
🔗 Jira: your-company.atlassian.net

📋 5 story(ies) à créer...

  📝 Création: 'Test case generation with LLM'... ✅ DT-2
  📝 Création: 'Automation framework setup'... ✅ DT-3
  📝 Création: 'API & UI test development'... ✅ DT-4
  📝 Création: 'CI/CD integration'... ✅ DT-5
  📝 Création: 'Reporting & dashboards'... ✅ DT-6

======================================================================
RÉSUMÉ
======================================================================
✅ Succès: 5/5
======================================================================
```

**Remarque :** Les clés de story (DT-2, DT-3, etc.) doivent être utilisées dans `TASKS_TO_CREATE`.

### Créer des sous-tâches Jira

1. Éditez d'abord `create_jira_tasks.py` et mettez à jour les `parent_story_key` avec les vraies clés Jira (ex. DT-2 au lieu de DT-2) :

```python
TASKS_TO_CREATE = [
    {
        "parent_story_key": "DT-2",  # ← Remplacez par votre clé
        "summary": "Write prompt structure",
        "description": "...",
        "issuetype": "Sous-tâche"
    },
    # ... etc
]
```

2. Exécutez le script :

```bash
python create_jira_tasks.py
```

### Exécuter les tests Appium

```bash
python Testing\Functional_test\SuiteTest1.py
```

**Prérequis :**
- Appium server lancé : `appium` (ou `npx appium`)
- Android device/emulator connecté et accessible

### Générer les rapports

```bash
python Report\report_pdf\json_to_pdf.py
```

Génère `tests_report.tex` (et PDF si LaTeX installé).

### Regénérer les acceptance criteria

```bash
python generate_all_criteria.py
```

---

## 3. Scripts Jira en détail

### `create_jira_stories.py`

**Rôle :** Crée 5 stories prédéfinies sous un Epic Jira.

**Configuration requise dans `.env` :**
- `JIRA_DOMAIN`
- `PROJECT_KEY`
- `EPIC_KEY`
- `JIRA_EMAIL`
- `JIRA_API_TOKEN`

**Comportement :**
- ✅ Valide la configuration avant de créer
- ✅ Crée 5 stories (Test case generation, Framework setup, API & UI, CI/CD, Reporting)
- ✅ Affiche les clés Jira créées (ex. DT-2, DT-3...)
- ❌ Gère les erreurs HTTP 400/401/403/500 gracieusement

### `create_jira_tasks.py`

**Rôle :** Crée des sous-tâches (Sous-tâche) sous les stories.

**Configuration requise dans `.env` :**
- Même que `create_jira_stories.py`

**Étapes :**
1. Copiez les clés de story depuis la sortie de `create_jira_stories.py`
2. Éditez `TASKS_TO_CREATE` et remplacez les clés
3. Exécutez `python create_jira_tasks.py`

**Comportement :**
- ✅ Valide que chaque task a une `parent_story_key` valide
- ✅ Crée ~20 sous-tâches réparties sous les 5 stories
- ✅ Affiche un résumé final (succès/échecs)

---

## 4. Dépannage

### ❌ Erreur : `config.py not found`

**Cause :** Vous n'avez pas le fichier `config.py` ou vous lancez le script depuis un mauvais répertoire.

**Solution :**
- Assurez-vous que `config.py` est dans le même répertoire que `create_jira_stories.py`.
- Lancez depuis la racine du projet (`c:\Users\MSI\D17Testing\`).

### ❌ Erreur : `JIRA_DOMAIN not configured`

**Cause :** Variables `.env` manquantes ou par défaut.

**Solution :**
```bash
1. cp .env.example .env
2. Éditez .env avec vos valeurs réelles
3. python config.py  # Vérifiez
4. python create_jira_stories.py
```

### ❌ Erreur : `HTTP 401 Unauthorized`

**Cause :** `JIRA_EMAIL` ou `JIRA_API_TOKEN` incorrect.

**Solution :**
1. Vérifiez votre email Jira
2. Regénérez un token API : https://id.atlassian.com/manage/api-tokens
3. Mettez à jour `.env`
4. Testez à nouveau

### ❌ Erreur : `HTTP 403 Forbidden`

**Cause :** Utilisateur n'a pas de permission sur le projet ou l'Epic.

**Solution :**
1. Vérifiez que vous avez **Create Issue** permission sur le projet
2. Vérifiez que l'Epic (ex. DT-1) existe et que vous pouvez le voir
3. Contactez votre admin Jira si besoin

### ❌ Erreur : `HTTP 404 Not Found (Epic not found)`

**Cause :** `EPIC_KEY` incorrecte ou n'existe pas.

**Solution :**
1. Vérifiez la clé de l'Epic dans Jira (ex. DT-1, PROJ-10, etc.)
2. Assurez-vous que l'Epic est dans votre projet
3. Mettez à jour `.env` avec la clé correcte

### ⚠️ Avertissement : `Timeout (30s)`

**Cause :** Connexion lente ou Jira non accessible.

**Solution :**
1. Vérifiez votre connexion Internet
2. Vérifiez que `JIRA_DOMAIN` est accessible (ouvrez dans un navigateur)
3. Augmentez le timeout dans le code (modifier `timeout=30` en `timeout=60`)

---

## 📝 Notes supplémentaires

- **Fichier `config.py`** : Centralise toutes les configurations. Modifiez-le si besoin d'ajouter de nouvelles variables.
- **Fichier `.env.example`** : Template documenté. Mettez-le à jour si vous ajoutez de nouvelles variables.
- **Logging** : Les scripts affichent des messages clairs avec emojis pour meilleure lisibilité.
- **Retries** : Les scripts gèrent les timeouts et tentent des retries (voir `TestCaseGenerateConnect.py` pour exemple).

---

## 🔗 Ressources utiles

- [Documentation Jira API](https://developer.atlassian.com/cloud/jira/rest/v3/)
- [Appium Documentation](https://appium.io/)
- [Google GenAI API](https://ai.google.dev/)

---

**Dernière mise à jour :** 2025-12-16
