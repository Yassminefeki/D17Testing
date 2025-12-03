from appium import webdriver
from appium.options.android import UiAutomator2Options
import time

# 1️⃣ Configuration Appium
options = UiAutomator2Options()
options.platform_name = "Android"
options.platform_version = "16"        # ⚠ Version Android de ton appareil
options.device_name = "RZCW81HN1XM"    # ⚠ Nom de ton appareil
options.app_package = "tn.mobipost"    # ⚠ Package de l'app
# options.app_activity = "tn.mobipost.MainActivity"  # ⚠ Mettre l'activité principale si nécessaire
options.automation_name = "UiAutomator2"
options.no_reset = True                 # Garde la session si déjà connecté

# 2️⃣ Connexion au serveur Appium
driver = webdriver.Remote("http://localhost:4723", options=options)
time.sleep(5)  # attendre le lancement de l'app

print("✅ Connected to the app successfully!")    

# 3️⃣ Fermer l'application
driver.quit() 
