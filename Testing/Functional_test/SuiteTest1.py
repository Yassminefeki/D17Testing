from appium import webdriver
from appium.options.android import UiAutomator2Options
import time

# 1️⃣ Options Appium
options = UiAutomator2Options()
options.platform_name = "Android"
options.platform_version = "16"
options.device_name = "RZCW81HN1XM"
options.app_package = "tn.mobipost"
options.app_activity = "tn.anypli.mobiposte.ui.activity.SplashScreenActivity"

# 2️⃣ Lancer Appium + ouvrir l'app
driver = webdriver.Remote("http://localhost:4723", options=options)
driver.implicitly_wait(10)

# 3️⃣ Attendre que la page de login charge
time.sleep(2)

# 4️⃣ Saisir le mot de passe
password_field = driver.find_element("id", "tn.mobipost:id/et_connexion_password")
password_field.click()
password_field.send_keys("test")   # 🔐 ton mot de passe ici

# 5️⃣ Cliquer sur "Valider"
validate_button = driver.find_element("id", "tn.mobipost:id/btn_connexion_validate")
validate_button.click()

# 6️⃣ Attendre le résultat
time.sleep(5)

# 7️⃣ Quitter
driver.quit()
