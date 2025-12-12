from appium import webdriver
from appium.options.android import UiAutomator2Options
import time

# 1️⃣ Options Appium (juste pour démarrer l'app)
options = UiAutomator2Options()
options.platform_name = "Android"
options.platform_version = "16"          
options.device_name = "RZCW81HN1XM"      
options.app_package = "tn.mobipost"
options.app_activity = "tn.anypli.mobiposte.ui.activity.SplashScreenActivity"

# 2️⃣ Lancer Appium + lancer l'application
driver = webdriver.Remote("http://localhost:4723", options=options)

# 3️⃣ Attendre que l'app s'ouvre
time.sleep(5)

# 4️⃣ Fermer
driver.quit()
