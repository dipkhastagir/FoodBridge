from helpers import *


def test(driver):
    open_admin_dashboard(driver)
    click(driver, "tab-users")
    click(driver, "block-3")
    accept_alert(driver)
    message = wait_for_message(driver)
    wait_until(driver, lambda d: "Blocked" in d.find_element(By.CSS_SELECTOR, "#user-3 .user-status").text)

    logout(driver)
    open_page(driver, "login.html")
    type_text(driver, "email", COLLECTOR2_EMAIL)
    type_text(driver, "password", COLLECTOR2_PASSWORD)
    click(driver, "loginBtn")
    login_message = wait_for_message(driver)
    passed = "blocked" in message and "blocked" in login_message and "login.html" in driver.current_url
    return passed, message + " | Login attempt: " + login_message


TEST_CASE = ("TC49", "Verify admin can block a user",
             "Block: Smile Foundation, then log in as smile@foodbridge.com", test)


def run():
    return run_test_module("Admin", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
