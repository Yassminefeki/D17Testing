# Documentation détaillée — Code et architecture

Date : 2025-12-16

## Objectif
Fournir une documentation complète du dépôt D17Testing : structure, composants, flux d'exécution, dépendances, et instructions opérationnelles pour générer des cas de test, exécuter des suites Appium, produire des rapports et créer des tickets Jira.

## Vue d'ensemble de l'architecture

Architecture logique (composants principaux) :

- **Génération de cas de test (LLM)** : scripts qui utilisent une API GenAI pour produire JSON de cas de test (`Testing/Test Case Generate/TestCaseGenerate*.py`). Ex. le générateur `TestCaseGenerateConnect.py` appelle l'API GenAI (clé `GEMINI_API_KEY`) et écrit `TestCaseConnect.json`.
- **Exécution des tests UI (Appium)** : suites Appium sous `Testing/Functional_test/` (ex. `SuiteTest1.py`) et utilitaires (`Connect_To_App.py`). Elles lisent des JSON de cas (ex. `TestCaseConnect.json`), pilotent une instance Appium et enregistrent résultats JSON.
- **Tests de performance & autres** : scripts dans `Testing/Performance_Test/` (ex. `d17_rush_hour.py`) pour charge/latence.
- **Gestion des user stories & critères** : scripts de génération et gestion (`manage_user_stories.py`, `generate_all_criteria.py`, dossiers `Android/...`) qui produisent/écrivent des `acceptance_criteria.md` et aident à standardiser les stories.
- **Intégration Jira** : scripts `create_jira_stories.py` et `create_jira_tasks.py` utilisent `.env` (variables Jira) pour créer issues via l'API REST Jira.
- **Reporting** : collecte JSON → conversion LaTeX/PDF via `Report/report_pdf/json_to_pdf.py` (utilise `pylatex`) qui génère `tests_report.tex` puis PDF si LaTeX disponible.
- **Données & Artéfacts** : `Testing/Test Case Generate/*.json`, `Testing/XML/*.xml`, `Testing/report/*.json`, `screenshots/`.

## Dépendances & prérequis

- Python 3.8+
- Outils externes : Appium server (v1.x/v2.x compatible avec UiAutomator2), Android SDK (adb), LaTeX (optionnel, pour générer PDF).
- Python packages listés dans `requirements.txt`: [requirements.txt](requirements.txt) (ex. `requests`, `python-dotenv`). D'autres libs sont utilisées au besoin (ex. `pylatex`, `appium-python-client`, `google-genai` si vous utilisez GenAI client).
- Variables d'environnement (fichier `.env` dans la racine, non fourni) :
  - `JIRA_DOMAIN`, `PROJECT_KEY`, `EPIC_KEY`, `JIRA_EMAIL`, `JIRA_API_TOKEN` (pour `create_jira_*.py`).
  - `GEMINI_API_KEY` (pour `TestCaseGenerateConnect.py` / GenAI).

## Flux d'exécution (scénario commun)

1. Génération des cas de test (optionnel)
   - Exécuter `TestCaseGenerateConnect.py` (ou équivalent) pour produire `TestCaseConnect.json`.
2. Exécution des tests UI
   - Lancer Appium server : assurer qu'Appium est accessible à `http://localhost:4723`.
   - Exécuter une suite (ex. `SuiteTest1.py`) ; la suite lit le JSON, exécute les cas, capture screenshots, puis écrit un rapport JSON.
3. Génération de rapports
   - Utiliser `Report/report_pdf/json_to_pdf.py` pour convertir le JSON en `.tex` (et PDF si LaTeX installé).
4. Jira (optionnel)
   - Exécuter `create_jira_stories.py` / `create_jira_tasks.py` pour créer issues automatiquement en utilisant la configuration `.env`.
5. Gestion des user stories
   - Utiliser `manage_user_stories.py` ou `generate_all_criteria.py` pour regénérer les `acceptance_criteria.md` depuis templates.

## Exécution — commandes utiles

- Installer les dépendances :

```bash
python -m pip install -r requirements.txt
# Installer en plus si nécessaire:
# pip install pylatex appium-python-client google-genai python-dotenv
```

- Lancer Appium (exemple, depuis Node):

```bash
appium
# ou si Appium est installé globalement: npx appium
```

- Exécuter une suite fonctionnelle (Windows PowerShell):

```powershell
python Testing\Functional_test\SuiteTest1.py
```

- Générer des cases de test via GenAI (nécessite clé):

```powershell
setx GEMINI_API_KEY "votre_clef"
python Testing\Test Case Generate\TestCaseGenerateConnect.py
```

- Regénérer tous les acceptance criteria:

```powershell
python generate_all_criteria.py
```

- Générer le rapport LaTeX (depuis le dossier `Report/report_pdf`):

```powershell
python Report\report_pdf\json_to_pdf.py
# puis (si LaTeX installé)
# pdflatex tests_report.tex
```

- Créer stories Jira (nécessite `.env` configuré correctement):

```powershell
python create_jira_stories.py
python create_jira_tasks.py
```

## Détails par fichier / module (extraits et responsabilités)

- [create_jira_stories.py](create_jira_stories.py)
  - **Rôle**: Crée des stories Jira prédéfinies via l'API REST. Lit `JIRA_*` depuis `.env`. Utilise `requests`.
  - **Points d'attention**: Validation basique des variables d'environnement, construction du payload en format Storage Document (Jira Cloud API v3). Gérer les erreurs HTTP.

- [create_jira_tasks.py](create_jira_tasks.py)
  - **Rôle**: Crée des sous-tâches sous des stories (doit adapter `parent_story_key`).
  - **Points d'attention**: Vérifier `parent_story_key` valide; la gestion des exceptions est en place (`raise_for_status`).

- [generate_all_criteria.py](generate_all_criteria.py)
  - **Rôle**: Script maître qui cherche les scripts `generate_acceptance_criteria.py` dans chaque dossier Android/test_* et les exécute.
  - **Points d'attention**: Utilise import dynamique (`importlib.util`) et change le CWD avant exécution pour que les scripts écrivent correctement.

- [manage_user_stories.py](manage_user_stories.py)
  - **Rôle**: Fournit une classe `UserStoryManager` pour parser `user_stories.md`, générer des `acceptance_criteria.md` à partir de templates et produire un rapport synthétique.
  - **Points d'attention**: Les templates sont codés en dur dans le script; on peut externaliser en YAML/JSON pour maintenabilité.

- [Testing/Connect_To_App.py](Testing/Connect_To_App.py)
  - **Rôle**: Exemple minimal d'init Appium (`UiAutomator2Options`) qui ouvre puis ferme la session. Utile comme snippet de setup.

- [Testing/Functional_test/SuiteTest1.py](Testing/Functional_test/SuiteTest1.py)
  - **Rôle**: Exemple d'exécution d'une suite de tests UI :
    - Lit `TestCaseConnect.json` (chemin absolu configuré).
    - Initialise Appium driver (`UiAutomator2Options`), exécute chaque test via `run_test_case`.
    - Logique de validation : vérifie présence de pop-up ou d'erreur inline, capture screenshots en cas d'échec et écrit le rapport JSON final.
  - **Points d'attention**: Chemins configurés en dur (`JSON_FILE`, `OUTPUT_REPORT`) — modifier si besoin pour portabilité. Assurez-vous qu'`AppiumBy.ID` et les IDs correspondent à l'app réelle.

- [Testing/Test Case Generate/TestCaseGenerateConnect.py](Testing/Test Case Generate/TestCaseGenerateConnect.py)
  - **Rôle**: Utilise le client GenAI (`google.genai`) pour demander un JSON conforme à un schéma (ex. 4 cas invalides). Gère erreurs 503 avec retries.
  - **Points d'attention**: Requiert la librairie et la clé API. Valider la structure renvoyée par le modèle avant l'utilisation.

- [Report/report_pdf/json_to_pdf.py](Report/report_pdf/json_to_pdf.py)
  - **Rôle**: Charge JSON de tests, crée un document LaTeX via `pylatex`, écrit `tests_report.tex`. Peut générer PDF si LaTeX installé.
  - **Points d'attention**: Le script lit un chemin absolu vers `rapport_connexion_d17.json` — ajuster si votre structure diffère.

## Schéma de données & formats

- Cas de test (JSON attendu par les suites) : tableau d'objets contenant au minimum `ID_Test`, `Titre_Test`, `Étapes_Test` (array), `Données_Test`, `Résultat_Attendu`.
- Rapport d'exécution (JSON produit) : pour chaque test -> `Statut_Execution` (PASS/FAIL/BLOCKED), `Date_Execution`, `Note_Defaut`, etc. Ce format est consommé par `json_to_pdf.py`.
- `acceptance_criteria.md` : format Markdown en Given/When/Then, un critère par user story.
- XMLs dans `Testing/XML/` : semblent contenir définitions d'interfaces et messages attendus — utilisés pour recherche de messages d'erreur/identifiants.

## Sécurité & confidentialité

- Ne pas committer `.env` avec clés (Jira API token, GEMINI_API_KEY).
- Vérifier que les logs/screenshots ne contiennent pas données sensibles avant archivage.

## Recommandations d'amélioration

- Paramétrer tous les chemins (actuellement absolus dans plusieurs fichiers) via un fichier de config central (`config.yaml` ou `.env`) pour améliorer portabilité.
- Externaliser templates d'`ACCEPTANCE_CRITERIA_TEMPLATES` dans `manage_user_stories.py` vers YAML/JSON.
- Ajouter validation stricte du JSON généré par GenAI (schéma JSON Schema) avant exécution des suites.
- Utiliser un runner (pytest) pour les suites fonctionnelles et reporter vers Allure pour meilleure traçabilité.
- Ajouter CI job (GitHub Actions) pour lancer `generate_all_criteria.py` et vérifier non-régression.

## Emplacement du document ajouté
Le document a été placé ici : `DOCUMENTATION/DETAILED_DOCUMENTATION.md` (ce fichier).

---

Si vous voulez, je peux :
- Générer une version PDF/Word de cette documentation;
- Transformer les chemins absolus en variables configurables et appliquer la modification sur les scripts (patch);
- Ajouter un fichier `README.md` complet à la racine reprenant ce contenu.

Quel(s) point(s) souhaitez-vous que j'approfondisse ou que j'automatise ensuite ?
