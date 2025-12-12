# -*- coding: utf-8 -*-
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ==================== CONFIG À CHANGER ====================
PASSWORD = "test"
options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name = "RZCW81HN1XM"
options.app_package = "tn.mobipost"
options.app_activity = "tn.anypli.mobiposte.ui.activity.SplashScreenActivity"
options.no_reset = True               # NE PAS réinitialiser l'app
options.new_command_timeout = 300
options.uiautomator2_server_launch_timeout = 60000
options.uiautomator2_server_install_timeout = 90000

driver = webdriver.Remote("http://localhost:4723", options=options)
wait = WebDriverWait(driver, 20)

try:
    print("\n=== DÉMARRAGE TEST : Connexion → Menu → Déconnexion ===\n")

    # 1. Attente splash
    time.sleep(8)

    # 2. Saisie du mot de passe (le numéro est déjà enregistré dans l'app)
    pwd_field = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, "tn.mobipost:id/et_connexion_password"))
    )
    pwd_field.clear()
    pwd_field.send_keys(PASSWORD)
    print("✔ Mot de passe saisi")

    # 3. Bouton "Valider"
    driver.find_element(AppiumBy.ID, "tn.mobipost:id/btn_connexion_validate").click()
    print("✔ Connexion en cours...")
    time.sleep(10)

    # 4. Vérification page accueil
    wait.until(
        EC.presence_of_element_located((AppiumBy.ID, "tn.mobipost:id/tv_item_home_fragment_account_sold"))
    )
    print("✔ Connecté avec succès → Accueil détecté")

    # 5. Ouvrir menu
    driver.find_element(AppiumBy.ID, "tn.mobipost:id/iv_ct_start").click()
    print("✔ Menu ouvert")
    time.sleep(3)

    # 6. Cliquer sur "Déconnexion"
    driver.find_element(
        AppiumBy.XPATH, "//android.widget.TextView[@text='Déconnexion']"
    ).click()
    print("✔ Déconnexion demandée")
    time.sleep(2)

    # 7. Confirmer déconnexion
    wait.until(EC.element_to_be_clickable((AppiumBy.ID, "tn.mobipost:id/btn_cancel")))
    driver.find_element(AppiumBy.ID, "tn.mobipost:id/btn_cancel").click()
    print("✔ Déconnexion confirmée")
    time.sleep(5)

    # 8. Vérifier retour page connexion
    try:
        driver.find_element(AppiumBy.ID, "tn.mobipost:id/et_connexion_password")
        print("✔ SUCCÈS : Retour à la page de connexion")
    except:
        print("❌ ERREUR : Pas revenu sur la page de connexion")

except Exception as e:
    driver.save_screenshot("ERREUR_DECONNEXION.png")
    print("\n❌ ERREUR :", e)

finally:
    print("\n=== Test terminé ===")
    input("Appuie sur Entrée pour fermer...")
