import os
import time
import json
from google import genai
from google.genai import types

# --- 1. CONFIGURATION ET CONTEXTE ---

# Clé API : Le client GenAI lit automatiquement la variable d'environnement GEMINI_API_KEY.
# Assurez-vous qu'elle est définie dans votre terminal avant d'exécuter.
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("❌ ERREUR: La variable d'environnement GEMINI_API_KEY n'est pas définie.")
    print("Veuillez l'ajouter avant d'exécuter le script.")
    exit()

# Contraintes de connexion D17 spécifiques
user_story = "Le système de connexion de D17 nécessite seulement un Mot de Passe (MDP). Le MDP doit être une chaîne alphanumérique (lettres et chiffres) de 4 à 6 caractères."

# Le prompt demande spécifiquement 4 cas invalides
prompt = f"""
En utilisant la User Story suivante, vous devez générer exactement 4 cas de test **INVALIDE** pour la fonctionnalité de connexion de D17.
Le format doit correspondre au schéma JSON fourni.

User Story: {user_story}

Les 4 cas invalides doivent couvrir:
1. Longueur trop courte (< 4).
2. Longueur trop longue (> 6).
3. Utilisation de caractères spéciaux (non-alphanumérique).
4. Champ vide.
"""

# --- 2. DÉFINITION DU SCHÉMA JSON DE SORTIE ---

test_case_schema = types.Schema(
    type=types.Type.ARRAY,
    description="Liste des cas de test invalides générés.",
    items=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "ID_Test": types.Schema(type=types.Type.STRING, description="Ex: TC-D17-INV-001"),
            "Titre_Test": types.Schema(type=types.Type.STRING, description="Ex: Mot de passe trop court"),
            "Étapes_Test": types.Schema(type=types.Type.ARRAY, items=types.Schema(type=types.Type.STRING), description="Liste des actions à effectuer (ex: 'Saisir un MDP de 3 caractères')."),
            "Données_Test": types.Schema(type=types.Type.STRING, description="La valeur saisie (Ex: '123' ou '[VIDE]')."),
            "Résultat_Attendu": types.Schema(type=types.Type.STRING, description="Le message d'erreur ou le comportement attendu par le système.")
        },
        required=["ID_Test", "Titre_Test", "Étapes_Test", "Données_Test", "Résultat_Attendu"]
    )
)

# --- 3. APPEL À L'API AVEC GESTION DES ERREURS (503) ---

OUTPUT_FILE = "TestCaseConnect.json"
MAX_RETRIES = 3
client = genai.Client()
test_cases = None

print("Début de la génération des cas de test invalides...")

for attempt in range(MAX_RETRIES):
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=test_case_schema,
            ),
        )

        # Si l'appel réussit, charger le JSON et sortir de la boucle
        test_cases = json.loads(response.text)
        break

    except Exception as e:
        error_detail = str(e)
        if "503 UNAVAILABLE" in error_detail:
            if attempt < MAX_RETRIES - 1:
                wait_time = 2 ** attempt
                print(f"⚠️ Tentative {attempt + 1}/{MAX_RETRIES} échouée (Erreur 503). Réessai dans {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"❌ Échec après {MAX_RETRIES} tentatives. Le modèle est surchargé. Veuillez réessayer plus tard.")
                exit()
        else:
            print(f"❌ Erreur critique inattendue : {e}")
            exit()

# --- 4. TRAITEMENT ET ENREGISTREMENT DE LA SORTIE ---

if test_cases:
    # 4.1 Enregistrement dans un fichier JSON
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(test_cases, f, ensure_ascii=False, indent=4)
        
    print(f"\n✅ Succès ! Les {len(test_cases)} cas de test invalides ont été enregistrés dans : {OUTPUT_FILE}")

    # 4.2 Affichage des titres pour vérification
    print("\n--- Aperçu des cas générés : ---")
    for i, tc in enumerate(test_cases):
        print(f"{i+1}. {tc.get('ID_Test', 'N/A')} : {tc.get('Titre_Test', 'N/A')}")