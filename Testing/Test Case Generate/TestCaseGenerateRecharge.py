import os
import time
import json
from google import genai
from google.genai import types

# --- 1. CONFIGURATION ET CONTEXTE ---

# Assurez-vous que la variable d'environnement GEMINI_API_KEY est définie.
if not os.getenv("GEMINI_API_KEY"):
    print("❌ ERREUR: La variable d'environnement GEMINI_API_KEY n'est pas définie.")
    print("Veuillez l'ajouter à votre environnement de travail avant d'exécuter.")
    exit()

# CONTEXTE DE RECHARGE TÉLÉPHONIQUE D17
context_recharge = """
Générer une liste complète de Cas de Test (positifs et négatifs) pour la fonctionnalité de 'Recharge téléphonique' de l'application D17, basée sur l'interface utilisateur fournie.

Les champs de l'écran sont :
1. Opérateur (Tunisie Telecom, Ooredoo, Orange) : Sélection obligatoire.
2. N° GSM à recharger : Doit être un numéro tunisien à 8 chiffres.
3. Montant de la recharge : Peut être un montant fixe prédéfini (ex: 5, 10, 20 TND) OU un montant saisi dans le champ 'Autre montant' (Montant > 1 TND).

Le scénario de test doit inclure :
- Un cas de succès pour un montant fixe.
- Un cas de succès pour 'Autre montant'.
- Un cas d'échec (N° GSM manquant ou invalide).
- Un cas d'échec (Opérateur non sélectionné).
- Un cas d'échec (Solde D17 insuffisant).
- Un cas d'échec (Montant minimum non atteint).
"""

# --- 2. DÉFINITION DU SCHÉMA JSON DE SORTIE ---

# Ce schéma garantit que le modèle renvoie un tableau structuré facile à lire
test_case_schema = types.Schema(
    type=types.Type.ARRAY,
    description="Liste des cas de test pour la fonctionnalité de recharge téléphonique.",
    items=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "ID_Test": types.Schema(type=types.Type.STRING, description="Ex: TC-RECH-001"),
            "Titre_Test": types.Schema(type=types.Type.STRING, description="Ex: Recharge succès avec montant fixe"),
            "Préconditions": types.Schema(type=types.Type.STRING, description="Ex: Compte D17 avec solde suffisant"),
            "Étapes_Test": types.Schema(type=types.Type.ARRAY, items=types.Schema(type=types.Type.STRING), description="Liste des actions à effectuer."),
            "Données_Test": types.Schema(type=types.Type.STRING, description="Ex: Opérateur: TT, N° GSM: 20123456, Montant: 5 TND"),
            "Résultat_Attendu": types.Schema(type=types.Type.STRING, description="Description du comportement attendu.")
        },
        required=["ID_Test", "Titre_Test", "Préconditions", "Étapes_Test", "Données_Test", "Résultat_Attendu"]
    )
)

# --- 3. APPEL À L'API AVEC GESTION DES ERREURS (503) ---

OUTPUT_FILE = "recharge_tests_d17.json"
MAX_RETRIES = 3
client = genai.Client()
test_cases = None

print("Début de la génération des cas de test de Recharge Téléphonique...")

for attempt in range(MAX_RETRIES):
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=context_recharge,
            config=types.GenerateContentConfig(
                # Force le modèle à renvoyer une structure JSON valide
                response_mime_type="application/json",
                response_schema=test_case_schema,
            ),
        )

        test_cases = json.loads(response.text)
        break # Succès, sortir de la boucle

    except Exception as e:
        error_detail = str(e)
        if "503 UNAVAILABLE" in error_detail:
            if attempt < MAX_RETRIES - 1:
                wait_time = 2 ** attempt
                print(f"⚠️ Tentative {attempt + 1}/{MAX_RETRIES} échouée (Erreur 503). Réessai dans {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"❌ Échec après {MAX_RETRIES} tentatives. Le modèle est surchargé.")
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

    # Aperçu des cas générés
    print("\n--- Aperçu des Titres de Test : ---")
    for i, tc in enumerate(test_cases):
        print(f"• {tc.get('ID_Test', 'N/A')} : {tc.get('Titre_Test', 'N/A')}")