import unittest
from connect import AppiumDriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class TestRechargeTelephonique(unittest.TestCase):
    def setUp(self):
        self.appium_driver = AppiumDriver()
        self.driver = self.appium_driver.start_driver()

    def tearDown(self):
        self.appium_driver.quit_driver()

    def test_recharge_telephonique_echec_code_errone(self):
        print("Running test_recharge_telephonique_echec_code_errone...")
        wait = WebDriverWait(self.driver, 10)

        try:
            # -------------------------------
            # Step 1 : Ouvrir le menu navbar
            # -------------------------------
            navbar_toggle = wait.until(
                EC.element_to_be_clickable((AppiumBy.ID, "tn.mobipost:id/iv_navbar_toggle"))
            )
            navbar_toggle.click()

            # ---------------------------------------------
            # Step 2 : Aller à "Recharge Téléphonique"
            # ---------------------------------------------
            recharge_button = wait.until(
                EC.element_to_be_clickable((AppiumBy.ID, "tn.mobipost:id/tv_mobile"))
            )
            recharge_button.click()

            # ---------------------------------------------
            # Step 3 : Choisir l’opérateur (Ooredoo)
            # ---------------------------------------------
            ooredoo_checkbox = wait.until(
                EC.element_to_be_clickable((AppiumBy.ID, "tn.mobipost:id/checkBox_mobile_refill_operator_ooredoo"))
            )
            ooredoo_checkbox.click()

            # -----------------------------------------------------
            # Step 4 : Saisir le numéro et le montant de recharge
            # -----------------------------------------------------
            phone_number_field = wait.until(
                EC.presence_of_element_located((AppiumBy.ID, "tn.mobipost:id/et_mobile_refill_gsm"))
            )
            phone_number_field.send_keys("20989020")

            amount_two_dinar = wait.until(
                EC.element_to_be_clickable((AppiumBy.ID, "tn.mobipost:id/iv_mobile_refill_amount_two_dinar"))
            )
            amount_two_dinar.click()

            # ---------------------------------------------
            # Step 5 : Cliquer sur "Recharger"
            # ---------------------------------------------
            recharger_button = wait.until(
                EC.element_to_be_clickable((AppiumBy.ID, "tn.mobipost:id/btn_mobile_refill_validate"))
            )
            recharger_button.click()

            # ---------------------------------------------
            # Step 6 : Saisir un PIN erroné
            # ---------------------------------------------
            pin_field = wait.until(
                EC.presence_of_element_located((AppiumBy.ID, "tn.mobipost:id/et_pin"))
            )
            pin_field.send_keys("1234")

            # ---------------------------------------------
            # Step 7 : Valider le PIN
            # ---------------------------------------------
            valider_button = wait.until(
                EC.element_to_be_clickable((AppiumBy.ID, "tn.mobipost:id/btn_ok"))
            )
            valider_button.click()

            # ---------------------------------------------
            # Step 8 : Vérifier le message d’erreur
            # ---------------------------------------------
            error_message = wait.until(
                EC.presence_of_element_located((AppiumBy.ID, "tn.mobipost:id/tv_msg"))
            )
            self.assertIn(
                "ECHEC DE L'OPÉRATION", error_message.text,
                "Le message d'erreur pour PIN incorrect n'est pas affiché"
            )

            # ---------------------------------------------
            # Step 9 : Fermer le message d’erreur
            # ---------------------------------------------
            error_ok_button = wait.until(
                EC.element_to_be_clickable((AppiumBy.ID, "tn.mobipost:id/btn_ok"))
            )
            error_ok_button.click()

            print("test_recharge_telephonique_echec_code_errone passed.")

        except (NoSuchElementException, TimeoutException) as e:
            self.fail(f"test_recharge_telephonique_echec_code_errone failed: Element not found - {e}")

        except Exception as e:
            self.fail(f"test_recharge_telephonique_echec_code_errone failed: {e}")


if __name__ == '__main__':
    unittest.main()
