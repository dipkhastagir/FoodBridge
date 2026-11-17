from helpers import *


def test(driver):
    fill_signup_form(driver, "Prefix Test", "prefix012@gmail.com", "01211223344", "donor", "Banani", "Road 11", "pass1234", "pass1234")
    validation = get_validation_message(driver, "phone")
    return validation != "" and "signup.html" in driver.current_url, "Browser message: " + validation


TEST_CASE = ("TC64", "Verify signup with mobile prefix 012 (not a valid operator)",
             "Mobile: 01211223344", test)


def run():
    return run_test_module("Sign Up", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
