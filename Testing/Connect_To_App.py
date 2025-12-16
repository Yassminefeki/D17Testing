from appium import webdriver
from appium.options.android import UiAutomator2Options
import time

options = UiAutomator2Options()
options.platform_name = "Android"
options.platform_version = "16"          
options.device_name = "RZCW81HN1XM"      
options.app_package = "tn.mobipost"
options.app_activity = "tn.anypli.mobiposte.ui.activity.SplashScreenActivity"
driver = webdriver.Remote("http://localhost:4723", options=options)
time.sleep(5)
driver.quit()
