from appium import webdriver
from appium.options.android import UiAutomator2Options
import time

# 1️⃣ Configuration Appium
options = UiAutomator2Options()

# Configuration du device
options.platform_name = "Android"
options.platform_version = "16"       
options.device_name = "RZCW81HN1XM"     

# Configuration de l'application
options.app_package = "tn.mobipost"      
# options.app_activity = "tn.mobipost.MainActivity" 

# Options supplémentaires
options.automation_name = "UiAutomator2"
options.no_reset = True          
# 2️⃣ Connexion au serveur Appium
driver = webdriver.Remote("http://localhost:4723", options=options)

time.sleep(5)  # temps de lancement

print("✅ Connected to the app successfully!")

# 3️⃣ Fermer l'application
driver.quit()
print("🔚 App closed successfully!")
