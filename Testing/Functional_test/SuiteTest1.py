# -*- coding: utf-8 -*-
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import json
import os
from datetime import datetime

# --- CONFIGURATION (Ne pas toucher aux chemins pour l'exécution) ---
# Vous avez défini les chemins d'accès absolus, je les laisse tels quels.
JSON_FILE = r"C:\Users\MSI\D17Testing\Testing\Test Case Generate\TestCaseConnect.json"
OUTPUT_REPORT = rf"C:\Users\MSI\D17Testing\Testing\report\rapport_connexion_d17.json"
SCREENSHOT_DIR = "screenshots" # Chemin relatif, le répertoire sera créé là où le script est exécuté

# --- LOCATORS SPÉCIFIQUES D17 ---
PASSWORD_FIELD_ID = "tn.mobipost:id/et_connexion_password"
VALIDATE_BUTTON_ID = "tn.mobipost:id/btn_connexion_validate"
# Locator pour l'erreur de validation (sous le champ MDP)
INLINE_ERROR_ID = "tn.mobipost:id/tv_connexion_invalidate_password" 
# Locator pour le pop-up (MDP incorrect/Veuillez vérifier vos données)
POPUP_MESSAGE_ID = "tn.mobipost:id/tv_msg"
POPUP_OK_BUTTON_ID = "tn.mobipost:id/btn_ok"

# --- 1. SETUP DRIVER ---
def setup_driver():
    # ... (Votre code setup_driver est correct, pas de changement nécessaire) ...
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.platform_version = "16"
    options.device_name = "RZCW81HN1XM"
    options.app_package = "tn.mobipost"
    options.app_activity = "tn.anypli.mobiposte.ui.activity.SplashScreenActivity"
    options.no_reset = True
    options.new_command_timeout = 300

    print("Démarrage du driver Appium...")
    driver = webdriver.Remote("http://localhost:4723", options=options)
    driver.implicitly_wait(10)
    return driver

# --- 2. RUN SINGLE TEST CASE (Logique de vérification adaptée) ---
def run_test_case(driver, test_data):
    password = test_data['Données_Test']
    test_id = test_data['ID_Test']
    
    # Initialisation du résultat
    test_data['Statut_Execution'] = 'FAIL'
    test_data['Date_Execution'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    test_data['Note_Defaut'] = 'Étape de test non atteinte (Erreur Appium ou initialisation).'

    try:
        print(f"\n--- EXÉCUTION DE {test_id}: {test_data['Titre_Test']} ---")
        wait = WebDriverWait(driver, 15)

        # ⚡ Attendre que la page de login soit visible
        password_field = wait.until(EC.presence_of_element_located((AppiumBy.ID, PASSWORD_FIELD_ID)))

        # Saisir le mot de passe
        password_field.clear()
        if password != "[VIDE]":
            password_field.send_keys(password)
            print(f"Saisie du MDP: '{password}'")
        else:
            print("Saisie du MDP: [VIDE]")

        # Cliquer sur "Valider"
        validate_button = driver.find_element(AppiumBy.ID, VALIDATE_BUTTON_ID)
        validate_button.click()
        print("Bouton 'Valider' cliqué.")

        # --- LOGIQUE DE VÉRIFICATION ADAPTÉE ---

        # 1. Vérification du Succès (Cas Positifs)
        # Si le MDP est valide, l'écran de connexion doit disparaître et l'élément suivant doit apparaître.
        # Pour les tests INVALIDES, on attend que l'écran NE disparaisse PAS.
        try:
            # Si le test est un test POSITIF (qui n'est pas dans votre JSON actuel, mais pour complétude)
            # if test_data.get('Scenario_Type') == 'POSITIF':
            #     # Attendre la disparition de l'écran de connexion
            #     wait.until(EC.invisibility_of_element_located((AppiumBy.ID, VALIDATE_BUTTON_ID)))
            #     test_data['Statut_Execution'] = 'PASS'
            #     test_data['Note_Defaut'] = "Connexion réussie. Écran d'accueil chargé."
            #     return test_data # Sortir de la fonction
            
            # Pour les tests INVALIDES, nous attendons 2 types d'erreurs: Pop-up ou Erreur Inline
            pass # Continuer pour vérifier les erreurs

        except TimeoutException:
             # Si le bouton Valider ne disparaît pas, c'est bon pour un test INVALIDE.
             pass 

        # 2. Vérification des Erreurs de Validation (Pop-up ou Inline)
        
        # A. Chercher le Pop-up (Erreur transactionnelle comme 'Veuillez vérifier vos données')
        try:
            popup_message = wait.until(EC.presence_of_element_located((AppiumBy.ID, POPUP_MESSAGE_ID))).text
            
            # Pop-up trouvé, cliquer sur OK pour fermer
            driver.find_element(AppiumBy.ID, POPUP_OK_BUTTON_ID).click()

            # Vérification du résultat
            if "VÉRIFIER VOS DONNÉES" in popup_message or "INCORRECT" in popup_message:
                test_data['Statut_Execution'] = 'PASS'
                test_data['Note_Defaut'] = f"Erreur Pop-up transactionnelle détectée : '{popup_message}'"
            else:
                test_data['Statut_Execution'] = 'FAIL'
                test_data['Note_Defaut'] = f"Pop-up détecté, mais message inattendu: '{popup_message}'"
                driver.save_screenshot(f"{SCREENSHOT_DIR}/{test_id}_FAIL_POPUP.png")
            return test_data # Sortir de la fonction après traitement du pop-up

        except TimeoutException:
            # B. Si pas de Pop-up, chercher l'Erreur Inline (Longueur, Vide, Caractères)
            try:
                error_element = driver.find_element(AppiumBy.ID, INLINE_ERROR_ID)
                actual_error_text = error_element.text
                print(f"Erreur Inline détectée: '{actual_error_text}'")

                # Mots-clés pour valider l'erreur (basé sur vos XML)
                expected_phrases = ["obligatoire", "4 à 6 caractères", "alphanumérique"]
                
                if any(phrase in actual_error_text for phrase in expected_phrases):
                    test_data['Statut_Execution'] = 'PASS'
                    test_data['Note_Defaut'] = f"Erreur Inline attendue détectée : '{actual_error_text}'"
                else:
                    test_data['Statut_Execution'] = 'FAIL'
                    test_data['Note_Defaut'] = f"Erreur Inline détectée, mais message inattendu: '{actual_error_text}'"
                    driver.save_screenshot(f"{SCREENSHOT_DIR}/{test_id}_FAIL_INLINE.png")

            except NoSuchElementException:
                # C. Échec si aucune erreur n'a été détectée (ni pop-up, ni inline)
                test_data['Statut_Execution'] = 'FAIL'
                test_data['Note_Defaut'] = "Échec : Le test est INVALIDE, mais aucune erreur (Pop-up ou Inline) n'a été détectée après validation."
                driver.save_screenshot(f"{SCREENSHOT_DIR}/{test_id}_FAIL_AUCUNE_ERREUR.png")

        except Exception as e:
            # Erreur inattendue durant la vérification
            test_data['Statut_Execution'] = 'BLOCKED'
            test_data['Note_Defaut'] = f"Erreur critique lors de la vérification : {str(e)[:150]}..."
            driver.save_screenshot(f"{SCREENSHOT_DIR}/{test_id}_BLOCKED_VERIF.png")

    except Exception as e:
        # Erreur Appium ou crash au début du test
        test_data['Statut_Execution'] = 'BLOCKED'
        test_data['Note_Defaut'] = f"Test bloqué ou plantage Appium : {str(e)[:150]}..."
        driver.save_screenshot(f"{SCREENSHOT_DIR}/{test_id}_BLOCKED_GLOBAL.png")

    return test_data

# --- 3. MAIN FUNCTION ---
def main():
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)

    # ... (Le code de chargement JSON et de sauvegarde du rapport est correct) ...
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            all_tests = json.load(f)
    except FileNotFoundError:
        print(f"❌ ERREUR: Fichier JSON non trouvé : {JSON_FILE}")
        return
    except json.JSONDecodeError:
        print(f"❌ ERREUR: Fichier JSON invalide : {JSON_FILE}")
        return

    driver = None
    try:
        driver = setup_driver()
        results = []

        for test_case in all_tests:
            result_case = run_test_case(driver, test_case)
            results.append(result_case)

            # 🔄 Revenir au SplashScreen pour le prochain test
            # C'est la meilleure pratique pour s'assurer que l'état initial est propre.
            try:
                driver.execute_script("mobile: terminateApp", {"appId": "tn.mobipost"})
                time.sleep(1)
                driver.execute_script("mobile: activateApp", {"appId": "tn.mobipost"})
                time.sleep(2)
            except Exception as e:
                print(f"⚠️ AVERTISSEMENT: Échec de la réinitialisation de l'application: {e}")


        # Sauvegarder le rapport final
        with open(OUTPUT_REPORT, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)

        print("\n" + "="*50)
        print(f"RAPPORT TERMINÉ. {len(results)} tests exécutés.")
        print(f"Résultats stockés dans : {OUTPUT_REPORT}")
        print("="*50)

    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()