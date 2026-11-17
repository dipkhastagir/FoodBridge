from helpers import *


def test(driver):
    fill_signup_form(driver, "No Area", "noarea@gmail.com", "01711000008", "donor", "", "Road 11", "pass1234", "pass1234")
    validation = get_validation_message(driver, "area")
    return validation != "" and "signup.html" in driver.current_url, "Browser message: " + validation


TEST_CASE = ("TC71", "Verify signup without selecting an area",
             "Area: (not selected), other fields valid", test)


def run():
    return run_test_module("Sign Up", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
