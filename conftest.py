import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import os

@pytest.fixture
def driver(request):
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # options.add_argument("--headless")  # Uncomment for headless

    # Use correct keyword argument 'version' to specify ChromeDriver version
    service = Service(ChromeDriverManager().install())  # specify exact version if needed
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)

    # request.node.driver = driver
    yield driver
    driver.quit()

# ⛔ Automatic screenshot capture + embed in HTML report
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to attach screenshots to pytest-html report on test failure."""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = getattr(item, "driver", None)
        if driver:
            os.makedirs("screenshots", exist_ok=True)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            test_name = item.name.replace("/", "_").replace("\\", "_")
            screenshot_path = os.path.join("screenshots", f"{test_name}_{timestamp}.png")

            driver.save_screenshot(screenshot_path)
            print(f"\n📸 Screenshot saved: {screenshot_path}")

            if hasattr(rep, "extra"):
                from pytest_html import extras
                rep.extra.append(extras.image(screenshot_path))
