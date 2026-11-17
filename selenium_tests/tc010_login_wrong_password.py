from helpers import *


def test(driver):
    fill_login_form(driver, DONOR_EMAIL, "wrong123")
    message = wait_for_message(driver)
    return message == "Invalid email or password." and "login.html" in driver.current_url, message


TEST_CASE = ("TC10", "Verify login with wrong password",
             "Email: donor@foodbridge.com, Password: wrong123", test)


def run():
    return run_test_module("Login", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
