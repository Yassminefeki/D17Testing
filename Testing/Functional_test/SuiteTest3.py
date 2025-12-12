# -*- coding: utf-8 -*-
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ==================== CONFIG (À CHANGER UNE SEULE FOIS) ====================
NUMERO    = "54478170"     # ← ton numéro à recharger (ici pour Orange : commence par 5)
MONTANT   = "2"            # "1", "2", "5" ou autre (ex: "10")
OPERATEUR = "orange"       # ooredoo → 2X | orange → 5X | telecom → 9X
PIN_D17   = "1234"         # ← TON VRAI CODE CONFIDENTIEL D17
# ==========================================================================

# Vérification immédiate du numéro vs opérateur
def check_numero():
    if len(NUMERO) != 8 or not NUMERO.isdigit():
        print("ERREUR : Le numéro doit avoir 8 chiffres !")
        exit()
    debut = NUMERO[0]
    attendu = {"ooredoo": "2", "orange": "5", "telecom": "9"}[OPERATEUR]
    if debut != attendu:
        print(f"ERREUR : Numéro {NUMERO} commence par {debut} → doit commencer par {attendu} pour {OPERATEUR.upper()} !")
        exit()
    print(f"Numéro {NUMERO} valide pour {OPERATEUR.upper()}")

check_numero()

# ==================== Démarrage Appium (déjà connectée) ====================
options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name = "RZCW81HN1XM"
options.app_package = "tn.mobipost"
options.app_activity = "tn.anypli.mobiposte.ui.activity.MainActivity"  # écran d'accueil connecté
options.no_reset = True
options.new_command_timeout = 300

driver = webdriver.Remote("http://localhost:4723", options=options)
wait = WebDriverWait(driver, 10)  # wait global pour les éléments

try:
    print("Début de la recharge... Attente chargement page d'accueil (10s max)")
    time.sleep(6)  # temps supplémentaire pour charger l'accueil connecté

    # 1. Ouvrir le menu (3 traits en bas à droite) - VERSION BLINDÉE
    menu_ouvert = False
    for menu_id in ["tn.mobipost:id/iv_navbar_toggle", "tn.mobipost:id/iv_ct_end_right", "tn.mobipost:id/nav_menu", "android:id/nav_menu"]:
        try:
            element = wait.until(EC.element_to_be_clickable((AppiumBy.ID, menu_id)))
            element.click()
            menu_ouvert = True
            print("Menu ouvert via ID :", menu_id)
            break
        except:
            continue
    
    if not menu_ouvert:
        # Fallback ultime : tap direct sur les coordonnées (bas droite, testé sur 1080x2340)
        print("Fallback : tap direct sur menu bas-droite")
        driver.tap([(1020, 2200)])  # coin bas-droite
        menu_ouvert = True
    
    if not menu_ouvert:
        # Debug : affiche le XML de la page pour voir ce qui cloche
        print("DEBUG : Page actuelle (premiers 2000 chars du XML) :")
        print(driver.page_source[:2000])
        raise Exception("Impossible d'ouvrir le menu - vérifie le XML ci-dessus")
    
    time.sleep(2)

    # 2. Aller sur Recharge téléphonique - BLINDÉ
    recharge_clique = False
    for xpath in [
        "//*[contains(@text,'Recharge') and contains(@text,'téléphonique')]",
        "//android.widget.TextView[contains(@text,'Recharge')]",
        "//*[@resource-id='tn.mobipost:id/tv_mobile']"
    ]:
        try:
            element = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, xpath)))
            element.click()
            recharge_clique = True
            print("Page recharge ouverte via XPath :", xpath[:50] + "...")
            break
        except:
            continue
    
    if not recharge_clique:
        driver.tap([(900, 1050)])  # centre de la tuile
        print("Fallback : tap direct sur tuile recharge")
    
    time.sleep(3)

    # 3. Sélectionner opérateur - BLINDÉ
    op_id = f"tn.mobipost:id/checkBox_mobile_refill_operator_{OPERATEUR}"
    try:
        element = wait.until(EC.element_to_be_clickable((AppiumBy.ID, op_id)))
        element.click()
        print(f"Opérateur {OPERATEUR.upper()} sélectionné")
    except:
        # Fallback coords (testées sur ton device)
        coords = {"ooredoo": (690, 726), "orange": (861, 726), "telecom": (529, 726)}
        driver.tap([coords[OPERATEUR]])
        print(f"Fallback tap sur {OPERATEUR.upper()}")
    
    time.sleep(1)

    # 4. Saisir numéro
    phone_field = wait.until(EC.presence_of_element_located((AppiumBy.ID, "tn.mobipost:id/et_mobile_refill_gsm")))
    phone_field.clear()
    phone_field.send_keys(NUMERO)
    print(f"Numéro {NUMERO} saisi")
    time.sleep(1)

    # 5. Choisir montant - BLINDÉ
    if MONTANT in ["1", "2", "5"]:
        amount_id = "one_dinar" if MONTANT == "1" else f"{MONTANT}_dinar"
        try:
            element = wait.until(EC.element_to_be_clickable((AppiumBy.ID, f"tn.mobipost:id/iv_mobile_refill_amount_{amount_id}")))
            element.click()
        except:
            # Fallback coords
            coords = {"1": (270, 1146), "2": (540, 1146), "5": (810, 1146)}
            driver.tap([coords[MONTANT]])
        print(f"Montant {MONTANT} DT sélectionné")
    else:
        other_field = wait.until(EC.presence_of_element_located((AppiumBy.ID, "tn.mobipost:id/et_mobile_refill_other_amount")))
        other_field.send_keys(MONTANT)
        print(f"Montant personnalisé {MONTANT} DT saisi")
    time.sleep(1)

    # 6. Cliquer sur Recharger
    btn_recharge = wait.until(EC.element_to_be_clickable((AppiumBy.ID, "tn.mobipost:id/btn_mobile_refill_validate")))
    btn_recharge.click()
    print("Bouton 'Recharger' cliqué")
    time.sleep(3)

    # 7. Saisir PIN + Valider
    pin_field = wait.until(EC.presence_of_element_located((AppiumBy.ID, "tn.mobipost:id/et_pin")))
    pin_field.clear()
    pin_field.send_keys(PIN_D17)
    time.sleep(0.5)
    
    btn_ok = wait.until(EC.element_to_be_clickable((AppiumBy.ID, "tn.mobipost:id/btn_ok")))
    btn_ok.click()
    print("PIN saisi et validé")
    time.sleep(4)

    # ==================== VÉRIFICATION DU RÉSULTAT ====================
    # Cas 1 : Popup d'échec
    try:
        msg = wait.until(EC.presence_of_element_located((AppiumBy.ID, "tn.mobipost:id/tv_msg"))).text
        wait.until(EC.element_to_be_clickable((AppiumBy.ID, "tn.mobipost:id/btn_ok"))).click()  # fermer
        driver.save_screenshot("RECHARGE_ECHOUEE.png")
        print(f"RECHARGE ÉCHOUÉE → {msg}")
        exit()
    except:
        pass

    # Cas 2 : Retour sur page de saisie = échec
    try:
        wait.until(EC.presence_of_element_located((AppiumBy.ID, "tn.mobipost:id/et_mobile_refill_gsm")))
        driver.save_screenshot("RETOUR_PAGE_SAISIE.png")
        print("RECHARGE ÉCHOUÉE → Retour à la page de saisie (mauvais PIN ou solde insuffisant)")
        exit()
    except:
        pass

    # Succès !
    driver.save_screenshot("RECHARGE_REUSSIE.png")
    print(f"SUCCÈS TOTAL : Recharge {MONTANT} DT → {NUMERO} ({OPERATEUR.upper()}) effectuée !")

except Exception as e:
    driver.save_screenshot("ERREUR_CRITIQUE.png")
    print("ERREUR INATTENDUE :", e)
    # Debug XML si besoin
    print("DEBUG XML (premiers 2000 chars) :", driver.page_source[:2000])

finally:
    time.sleep(3)
    # driver.quit()
    print("Test terminé.")