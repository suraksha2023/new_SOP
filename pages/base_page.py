# pages/base_page.py
import os
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    def snap(self, step_name):
        """Take screenshot with timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        os.makedirs("screenshots", exist_ok=True)
        file_path = os.path.join("screenshots", f"{step_name}_{timestamp}.png")
        self.driver.save_screenshot(file_path)
        print(f"📸 Screenshot saved: {file_path}")

    def wait_for_document(self, title):
        """Wait until document appears in Under-Review Docs table."""
        doc_locator = (By.XPATH, f"//a[normalize-space(text())='{title}']")
        print(f"⏳ Waiting for document '{title}' to appear...")
        self.wait.until(EC.visibility_of_element_located(doc_locator))
        self.wait.until(EC.element_to_be_clickable(doc_locator))
        print(f"✅ Document '{title}' is now visible and clickable.")
