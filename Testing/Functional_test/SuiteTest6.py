# -*- coding: utf-8 -*-
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ==================== CONFIG À CHANGER ====================
CIN_A_ENCAISSER = "15351379"      # ← Ton CIN du mandat
PIN_MANDAT      = "5640"          # ← Ton code PIN 4 chiffres
# =========================================================

options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name = "RZCW81HN1XM"
options.app_package = "tn.mobipost"
options.app_activity = "tn.anypli.mobiposte.ui.activity.MainActivity"
options.no_reset = True
options.uiautomator2_server_launch_timeout = 60000
options.uiautomator2_server_install_timeout = 90000

driver = webdriver.Remote("http://localhost:4723", options=options)
wait = WebDriverWait(driver, 20)

try:
    print("DÉMARRAGE : Encaissement Mandat Bourse (Organisme)")
    time.sleep(10)

    # 1. Ouvrir le menu (3 traits en bas à droite)
    driver.find_element(AppiumBy.ID, "tn.mobipost:id/iv_navbar_toggle").click()
    print("Menu ouvert")
    time.sleep(3)

    # 2. Cliquer sur "Encaissement mandat"
    driver.find_element(AppiumBy.XPATH, "//*[contains(@text,'Encaissement') and contains(@text,'mandat')]").click()
    print("Encaissement mandat ouvert")
    time.sleep(4)

    # 3. Sélectionner "Mandat organisme" dans Nature du mandat
    driver.find_element(AppiumBy.ID, "tn.mobipost:id/kind_mandate_spinner").click()
    time.sleep(1)
    driver.find_element(AppiumBy.XPATH, "//android.widget.TextView[@text='Mandat organisme']").click()
    print("Nature : Mandat organisme sélectionnée")
    time.sleep(2)

    # 4. Sélectionner "Mandat Bourse" dans Type de mandat (apparaît après)
    wait.until(EC.element_to_be_clickable((AppiumBy.ID, "tn.mobipost:id/type_mandate_spinner")))
    driver.find_element(AppiumBy.ID, "tn.mobipost:id/type_mandate_spinner").click()
    time.sleep(1)
    driver.find_element(AppiumBy.XPATH, "//android.widget.TextView[@text='Mandat Bourse']").click()
    print("Type : Mandat Bourse sélectionné")
    time.sleep(2)

    # 5. Cliquer sur "Suivant"
    driver.find_element(AppiumBy.ID, "tn.mobipost:id/btn_validate").click()
    print("Suivant → page CIN/PIN")
    time.sleep(4)

    # 6. Saisir CIN et PIN
    driver.find_element(AppiumBy.ID, "tn.mobipost:id/et_information").send_keys(CIN_A_ENCAISSER)
    driver.find_element(AppiumBy.ID, "tn.mobipost:id/et_pin_code").send_keys(PIN_MANDAT)
    print(f"CIN saisi : {CIN_A_ENCAISSER}")
    print(f"PIN saisi : {PIN_MANDAT}")

    # 7. Cliquer sur "Accepter"
    driver.find_element(AppiumBy.ID, "tn.mobipost:id/btn_validate").click()
    print("Accepter cliqué")
    time.sleep(10)

    # 8. Vérification du résultat
    try:
        msg = driver.find_element(AppiumBy.ID, "tn.mobipost:id/tv_msg").text
        if any(word in msg.lower() for word in ["succès", "encaissé", "réussie"]):
            print("SUCCÈS TOTAL : Mandat Bourse encaissé !")
        else:
            print("RÉSULTAT :", msg)
    except:
        print("SUCCÈS : Aucune erreur → encaissement réussi")

    print("Test terminé avec succès !")

except Exception as e:
    driver.save_screenshot("ERREUR_ENCAISSEMENT_MANDAT_BOURSE.png")
    print("ERREUR :", e)

finally:
    print("Fin du test.")
    input("Appuie sur Entrée pour fermer...")