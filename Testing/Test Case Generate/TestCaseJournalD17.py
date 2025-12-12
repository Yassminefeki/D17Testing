import os
import time
import json
from google import genai
from google.genai import types
from datetime import datetime

# --- 1. CONFIGURATION ET CONTEXTE ---

# Assurez-vous que la variable d'environnement GEMINI_API_KEY est définie.
if not os.getenv("GEMINI_API_KEY"):
    print("❌ ERREUR: La variable d'environnement GEMINI_API_KEY n'est pas définie.")
    print("Veuillez l'ajouter à votre environnement de travail avant d'exécuter.")
    exit()

# La Date de Fin est fixée à la date d'aujourd'hui
DATE_DU_JOUR = datetime.now().strftime("%d/%m/%Y")

# CONTEXTE SPÉCIFIQUE DU JOURNAL D17
context_journal = f"""
Générer une liste de Cas de Test (positifs et négatifs) pour la fonctionnalité de 'Téléchargement du Journal D17'.

RÈGLE ESSENTIELLE : L'utilisateur sélectionne uniquement la Date de Début. La Date de Fin est implicitement fixée à la Date du Jour : {DATE_DU_JOUR}.

Les scénarios de test doivent inclure :
1. Cas de Succès (Date de Début valide).
2. Cas de Succès (Date de Début égale à la Date du Jour).
3. Cas d'Échec (Date de Début future).
4. Cas d'Échec (Date de Début trop ancienne, dépassant la limite maximale de l'historique, estimée à 1 an).
5. Cas d'Échec (Période sans aucune transaction).
"""

# --- 2. DÉFINITION DU SCHÉMA JSON DE SORTIE ---

test_case_schema = types.Schema(
    type=types.Type.ARRAY,
    description="Liste des cas de test pour la fonctionnalité de Journal D17.",
    items=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "ID_Test": types.Schema(type=types.Type.STRING, description="Ex: TC-JNL-001"),
            "Titre_Test": types.Schema(type=types.Type.STRING, description="Ex: Téléchargement succès (période 1 mois)"),
            "Préconditions": types.Schema(type=types.Type.STRING, description="Ex: Compte actif, transactions disponibles."),
            "Étapes_Test": types.Schema(type=types.Type.ARRAY, items=types.Schema(type=types.Type.STRING), description="Liste des actions à effectuer (ex: Cliquer sur icône, Sélectionner Date de Début)."),
            "Date_Debut_Saisie": types.Schema(type=types.Type.STRING, description="La date que l'utilisateur doit saisir/sélectionner."),
            "Date_Fin_Implicite": types.Schema(type=types.Type.STRING, description="La Date de Fin utilisée par le système (Aujourd'hui)."),
            "Résultat_Attendu": types.Schema(type=types.Type.STRING, description="Description du comportement attendu.")
        },
        required=["ID_Test", "Titre_Test", "Préconditions", "Étapes_Test", "Date_Debut_Saisie", "Date_Fin_Implicite", "Résultat_Attendu"]
    )
)

# --- 3. APPEL À L'API AVEC GESTION DES ERREURS (503) ---

OUTPUT_FILE = r"C:\Users\MSI\D17Testing\Testing\Test Case Generate\journal_d17_tests.json"
MAX_RETRIES = 3
client = genai.Client()
test_cases = None

print(f"Début de la génération. Date de Fin implicite : {DATE_DU_JOUR}")

for attempt in range(MAX_RETRIES):
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=context_journal,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=test_case_schema,
            ),
        )

        test_cases = json.loads(response.text)
        break # Succès

    except Exception as e:
        error_detail = str(e)
        if "503 UNAVAILABLE" in error_detail:
            if attempt < MAX_RETRIES - 1:
                wait_time = 2 ** attempt
                print(f"⚠️ Tentative {attempt + 1}/{MAX_RETRIES} échouée (Erreur 503). Réessai dans {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"❌ Échec après {MAX_RETRIES} tentatives. Le modèle est surchargé. Code non exécuté.")
                exit()
        else:
            print(f"❌ Erreur critique inattendue : {e}")
            exit()

# --- 4. TRAITEMENT ET ENREGISTREMENT DE LA SORTIE ---

if test_cases:
    # Enregistrement dans un fichier JSON
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(test_cases, f, ensure_ascii=False, indent=4)

    print(f"\n✅ Succès ! Les {len(test_cases)} cas de test ont été générés et enregistrés dans : {OUTPUT_FILE}")

    # Aperçu
    print("\n--- Aperçu des Cas de Test Générés : ---")
    for tc in test_cases:
        print(f"• ID: {tc['ID_Test']} | Titre: {tc['Titre_Test']}")
        print(f"  Période testée : {tc['Date_Debut_Saisie']} -> {tc['Date_Fin_Implicite']}")
        print("-" * 25)