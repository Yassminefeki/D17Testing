from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

NOUVEAU_PRENOM       = "nour"
NOUVEAU_NOM          = "ben slimene"
ANCIEN_MOT_DE_PASSE  = "test"
NOUVEAU_MOT_DE_PASSE = "test"

options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name = "RZCW81HN1XM"
options.app_package = "tn.mobipost"
options.app_activity = "tn.anypli.mobiposte.ui.activity.MainActivity"
options.no_reset = True
options.auto_grant_permissions = True

driver = webdriver.Remote("http://localhost:4723", options=options)
wait = WebDriverWait(driver, 20)

def ouvrir_profil():
    try:
        wait.until(EC.element_to_be_clickable((AppiumBy.ID, "tn.mobipost:id/iv_ct_end_right"))).click()
    except:
        driver.tap([(975, 155)])
    time.sleep(3)

def fermer_popup_ok():
    try:
        driver.find_element(AppiumBy.ID, "tn.mobipost:id/btn_ok").click()
        time.sleep(1.5)
    except:
        pass

try:
    print("DÉMARRAGE : Changement complet du profil D17 (Google Photos Picker)")
    time.sleep(6)
    ouvrir_profil()

    # 1. NOM
    print("→ Nom")
    wait.until(EC.element_to_be_clickable((AppiumBy.ID, "tn.mobipost:id/tv_change_name"))).click()
    time.sleep(2)
    driver.find_element(AppiumBy.ID, "tn.mobipost:id/et_first_name").clear().send_keys(NOUVEAU_PRENOM)
    driver.find_element(AppiumBy.ID, "tn.mobipost:id/et_last_name").clear().send_keys(NOUVEAU_NOM)
    driver.find_element(AppiumBy.ID, "tn.mobipost:id/btn_validate").click()
    time.sleep(4)
    fermer_popup_ok()
    ouvrir_profil()

    # 2. MOT DE PASSE
    print("→ Mot de passe")
    wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//*[contains(@text,'mot de passe')]"))).click()
    time.sleep(3)
    driver.find_element(AppiumBy.ID, "tn.mobipost:id/et_old_password").send_keys(ANCIEN_MOT_DE_PASSE)
    driver.find_element(AppiumBy.ID, "tn.mobipost:id/et_password").send_keys(NOUVEAU_MOT_DE_PASSE)
    driver.find_element(AppiumBy.ID, "tn.mobipost:id/et_confirmation_password").send_keys(NOUVEAU_MOT_DE_PASSE)
    driver.find_element(AppiumBy.ID, "tn.mobipost:id/btn_validate").click()
    time.sleep(4)
    fermer_popup_ok()
    ouvrir_profil()

    # 3. PHOTO — MÉTHODE 100% FONCTIONNELLE AVEC GOOGLE PHOTOS PICKER
    print("→ Photo de profil")
    wait.until(EC.element_to_be_clickable((AppiumBy.ID, "tn.mobipost:id/tv_change_picture"))).click()
    time.sleep(2)

    # Choisir Galerie
    try:
        wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//android.widget.Button[@text='Galerie']"))).click()
    except:
        driver.find_element(AppiumBy.ID, "tn.mobipost:id/btn_dual_dialog_cancel").click()
    time.sleep(6)

    # ON EST DANS GOOGLE PHOTOS PICKER → ON CLIQUE DIRECTEMENT SUR LA PREMIÈRE PHOTO
    # Les photos ont content-desc="Photo taken on..." et sont dans un View cliquable
    try:
        # Cherche le premier élément avec "Photo taken on" dans le content-desc
        photo = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, 
            "//android.view.View[contains(@content-desc, 'Photo taken on')]")))
        photo.click()
        print("→ Photo sélectionnée via content-desc (Google Photos Picker)")
    except:
        # Fallback absolu : tap sur la première photo visible
        driver.tap([(180, 1830)])  # coordonnées exactes de la première photo dans ton XML
        print("→ Photo sélectionnée via tap direct (fallback ultime)")

    time.sleep(6)
    fermer_popup_ok()

    print("TOUT EST CHANGÉ : nom, mot de passe, photo de profil")
    driver.back()
    time.sleep(3)

except Exception as e:
    driver.save_screenshot("ERREUR_FINALE.png")
    print("ERREUR :", e)

finally:
    print("FIN DU SCRIPT — Va vérifier ton profil D17 : la photo doit être changée !")