from helpers import *


def test(driver):
    fill_login_form(driver, DONOR_EMAIL, "")
    validation = get_validation_message(driver, "password")
    return validation != "" and "login.html" in driver.current_url, "Browser message: " + validation


TEST_CASE = ("TC13", "Verify login with empty Password field",
             "Email: donor@foodbridge.com, Password: (blank)", test)


def run():
    return run_test_module("Login", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
