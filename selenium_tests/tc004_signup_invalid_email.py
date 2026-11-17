from helpers import *


def test(driver):
    fill_signup_form(driver, "Karim", "arpitasaha", "01711000000", "donor", "Banani", "Road 11", "pass1234", "pass1234")
    validation = get_validation_message(driver, "email")
    return validation != "", "Browser message: " + validation


TEST_CASE = ("TC04", "Verify signup with invalid email format",
             "Email: arpitasaha (no @)", test)


def run():
    return run_test_module("Sign Up", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
