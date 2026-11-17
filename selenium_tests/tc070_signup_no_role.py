from helpers import *


def test(driver):
    fill_signup_form(driver, "No Role", "norole@gmail.com", "01711000007", "", "Banani", "Road 11", "pass1234", "pass1234")
    validation = get_validation_message(driver, "role")
    return validation != "" and "signup.html" in driver.current_url, "Browser message: " + validation


TEST_CASE = ("TC70", "Verify signup without selecting a role",
             "Role: (not selected), other fields valid", test)


def run():
    return run_test_module("Sign Up", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
