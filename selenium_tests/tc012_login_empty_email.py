from helpers import *


def test(driver):
    fill_login_form(driver, "", DONOR_PASSWORD)
    validation = get_validation_message(driver, "email")
    return validation != "" and "login.html" in driver.current_url, "Browser message: " + validation


TEST_CASE = ("TC12", "Verify login with empty Email field",
             "Email: (blank), Password: donor123", test)


def run():
    return run_test_module("Login", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
