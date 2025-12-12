# -*- coding: utf-8 -*-
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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
    print("DÉMARRAGE : Test Journal D17 + Téléchargement PDF")
    time.sleep(10)

    # 1. Ouvrir Journal D17
    driver.find_element(AppiumBy.ID, "tn.mobipost:id/iv_navbar_journal").click()
    print("Journal ouvert")
    time.sleep(4)

    # 2. Téléchargement
    driver.find_element(AppiumBy.ID, "tn.mobipost:id/iv_ct_end_right").click()
    print("Icône téléchargement cliquée")
    time.sleep(3)

    # 3. Attendre le DatePicker
    print("Attente du sélecteur de date...")
    wait.until(EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.DatePicker")))
    print("DatePicker détecté !")

    # 4. Sélectionner la date de début : 01/12/2025
    # Jour (NumberPicker 1)
    day_picker = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.NumberPicker")[0]
    day_picker.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText").clear()
    day_picker.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText").send_keys("1")

    # Mois (NumberPicker 2) → Décembre
    month_picker = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.NumberPicker")[1]
    month_picker.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText").clear()
    month_picker.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText").send_keys("12")

    # Année (NumberPicker 3)
    year_picker = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.NumberPicker")[2]
    year_picker.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText").clear()
    year_picker.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText").send_keys("2025")

    print("Date de début : 01/12/2025")

    # 5. Cliquer sur OK
    driver.find_element(AppiumBy.ID, "tn.mobipost:id/btn_dual_dialog_ok").click()
    print("OK cliqué")
    time.sleep(3)

    # 6. Date de fin (même popup réapparaît)
    print("Sélection date de fin...")
    wait.until(EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.DatePicker")))

    day_picker = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.NumberPicker")[0]
    day_picker.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText").clear()
    day_picker.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText").send_keys("9")

    month_picker = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.NumberPicker")[1]
    month_picker.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText").clear()
    month_picker.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText").send_keys("12")

    year_picker = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.NumberPicker")[2]
    year_picker.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText").clear()
    year_picker.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText").send_keys("2025")

    print("Date de fin : 09/12/2025")

    driver.find_element(AppiumBy.ID, "tn.mobipost:id/btn_dual_dialog_ok").click()
    print("Validation finale envoyée...")
    time.sleep(12)

    print("PDF Journal D17 téléchargé avec succès !")
    print("Va dans Téléchargements → Journal_D17_01122025_09122025.pdf")

except Exception as e:
    driver.save_screenshot("ERREUR_JOURNAL_FINAL.png")
    print("ERREUR :", e)

finally:
    print("Test terminé.")
    input("Appuie sur Entrée pour fermer...")