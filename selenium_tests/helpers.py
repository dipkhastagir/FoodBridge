import os
import time
import json
import urllib.parse
import urllib.request

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

BASE_URL = "http://localhost:3000"
WAIT_TIME = 10
STEP_DELAY = 0.6
SCREENSHOT_FOLDER = "screenshots"

DONOR_EMAIL = "donor@foodbridge.com"
DONOR_PASSWORD = "Donor@FoodBridge26"
COLLECTOR_EMAIL = "collector@foodbridge.com"
COLLECTOR_PASSWORD = "Collector@FoodBridge26"
COLLECTOR2_EMAIL = "smile@foodbridge.com"
COLLECTOR2_PASSWORD = "Smile@FoodBridge26"
ADMIN_EMAIL = "admin@foodbridge.com"
ADMIN_PASSWORD = "Admin@FoodBridge26"

def start_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })
    options.add_argument("--disable-features=PasswordLeakDetection,PasswordCheck")
    options.add_argument("--disable-save-password-bubble")
    driver = webdriver.Chrome(options=options)
    return driver

def reset_database():
    request = urllib.request.Request(BASE_URL + "/api/test/reset", method="POST")
    with urllib.request.urlopen(request) as response:
        json.loads(response.read().decode())

def open_page(driver, page):
    driver.get(BASE_URL + "/" + page)
    time.sleep(STEP_DELAY)

def find(driver, element_id):
    return WebDriverWait(driver, WAIT_TIME).until(
        EC.presence_of_element_located((By.ID, element_id))
    )

def type_text(driver, element_id, text):
    box = find(driver, element_id)
    box.click()
    box.clear()
    if text != "":
        box.send_keys(text)
    time.sleep(STEP_DELAY / 3)

def choose_option(driver, element_id, value):
    dropdown = Select(find(driver, element_id))
    dropdown.select_by_value(value)
    time.sleep(STEP_DELAY / 3)

def click(driver, element_id):
    button = WebDriverWait(driver, WAIT_TIME).until(
        EC.element_to_be_clickable((By.ID, element_id))
    )
    button.click()
    time.sleep(STEP_DELAY)

def accept_alert(driver):
    alert = WebDriverWait(driver, WAIT_TIME).until(EC.alert_is_present())
    alert.accept()
    time.sleep(STEP_DELAY)

def wait_until(driver, condition):
    WebDriverWait(
        driver, WAIT_TIME,
        ignored_exceptions=[NoSuchElementException, StaleElementReferenceException]
    ).until(condition)

def get_validation_message(driver, element_id):
    box = find(driver, element_id)
    return driver.execute_script("return arguments[0].validationMessage;", box)

def wait_for_message(driver, element_id="message"):
    wait_until(driver, lambda d: d.find_element(By.ID, element_id).text.strip() != "")
    return driver.find_element(By.ID, element_id).text.strip()

def wait_for_url(driver, part_of_url):
    try:
        WebDriverWait(driver, WAIT_TIME).until(EC.url_contains(part_of_url))
        return True
    except Exception:
        return False

def wait_until_page_ready(driver, element_id):
    WebDriverWait(driver, WAIT_TIME).until(
        EC.visibility_of_element_located((By.ID, element_id))
    )
    time.sleep(STEP_DELAY)

def element_exists(driver, element_id):
    return len(driver.find_elements(By.ID, element_id)) > 0

def admin_give_code(driver, request_id, code):
    logout(driver)
    login(driver, ADMIN_EMAIL, ADMIN_PASSWORD)
    wait_until_page_ready(driver, "requestsBody")
    type_text(driver, "code-input-" + str(request_id), code)
    click(driver, "save-code-" + str(request_id))
    message = wait_for_message(driver)
    logout(driver)
    return message

def login(driver, email, password):
    open_page(driver, "login.html")
    type_text(driver, "email", email)
    type_text(driver, "password", password)
    click(driver, "loginBtn")
    wait_for_url(driver, "dashboard")

def logout(driver):
    driver.delete_all_cookies()

def save_screenshot(driver, test_id):
    try:
        os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)
        driver.save_screenshot(os.path.join(SCREENSHOT_FOLDER, test_id + ".png"))
    except Exception:
        pass

def print_result(test_id, title, test_data, passed, actual):
    print("=" * 70)
    print("Test Case :", test_id)
    print("Title     :", title)
    print("Test Data :", test_data)
    print("Actual    :", actual)
    print("Status    :", "Pass" if passed else "Fail")
    print()

def run_test_module(module_name, test_cases, login_as=None, logout_before_each=False):
    print()
    print("#" * 70)
    print("   MODULE:", module_name)
    print("#" * 70)

    reset_database()
    driver = start_browser()
    results = []

    try:
        if login_as:
            login(driver, login_as[0], login_as[1])

        for test_id, title, test_data, test_function in test_cases:
            if logout_before_each:
                open_page(driver, "index.html")
                logout(driver)
            try:
                passed, actual = test_function(driver)
            except Exception as error:
                passed, actual = False, "Error: " + str(error).split("\n")[0]
            save_screenshot(driver, test_id)
            print_result(test_id, title, test_data, passed, actual)
            results.append((test_id, module_name, title, test_data, actual, "Pass" if passed else "Fail"))
    finally:
        driver.quit()

    passed_count = sum(1 for r in results if r[5] == "Pass")
    print(f"{module_name}: {passed_count}/{len(results)} test cases passed.")
    return results


NEW_PASSWORD = "Fresh#Start2026"


def fill_signup_form(driver, name, email, phone, role, area, address, password, confirm):
    open_page(driver, "signup.html")
    wait_until(driver, lambda d: len(d.find_elements(By.CSS_SELECTOR, "#area option")) > 1)
    type_text(driver, "name", name)
    type_text(driver, "email", email)
    type_text(driver, "phone", phone)
    if role != "":
        choose_option(driver, "role", role)
    if area != "":
        choose_option(driver, "area", area)
    type_text(driver, "address", address)
    type_text(driver, "password", password)
    type_text(driver, "confirmPassword", confirm)
    click(driver, "signupBtn")


def fill_login_form(driver, email, password):
    open_page(driver, "login.html")
    type_text(driver, "email", email)
    type_text(driver, "password", password)
    click(driver, "loginBtn")


def open_donor_dashboard(driver):
    open_page(driver, "donor-dashboard.html")
    wait_until_page_ready(driver, "foodForm")
    wait_until(
        driver, lambda d: "Loading" not in d.find_element(By.ID, "foodTableBody").text
    )


def fill_food_form(driver, title, food_type, quantity, hours, location, notes):
    type_text(driver, "foodTitle", title)
    if food_type != "":
        choose_option(driver, "foodType", food_type)
    type_text(driver, "quantity", quantity)
    type_text(driver, "expiryHours", hours)
    type_text(driver, "location", location)
    type_text(driver, "notes", notes)
    click(driver, "saveFoodBtn")


def open_collector_dashboard(driver):
    open_page(driver, "collector-dashboard.html")
    wait_until_page_ready(driver, "searchBtn")
    wait_until(
        driver, lambda d: "Loading" not in d.find_element(By.ID, "claimsTableBody").text
    )


def visible_food_titles(driver):
    cards = driver.find_elements(By.CSS_SELECTOR, "#foodGrid .food-title")
    return [card.text for card in cards]


def open_profile(driver):
    open_page(driver, "profile.html")
    wait_until_page_ready(driver, "profileForm")


def send_request(driver, email, phone, message):
    open_page(driver, "forgot-password.html")
    type_text(driver, "email", email)
    type_text(driver, "phone", phone)
    type_text(driver, "requestMessage", message)
    click(driver, "sendRequestBtn")
    answer = wait_for_message(driver)
    wait_for_url(driver, "reset-password.html")
    return answer


def open_admin_dashboard(driver):
    login(driver, ADMIN_EMAIL, ADMIN_PASSWORD)
    wait_until_page_ready(driver, "requestsBody")
    wait_until(driver, lambda d: "Loading" not in d.find_element(By.ID, "usersBody").text)


def open_admin_tab(driver, tab_id, body_id):
    open_admin_dashboard(driver)
    click(driver, tab_id)
    wait_until(driver, lambda d: "Loading" not in d.find_element(By.ID, body_id).text)
