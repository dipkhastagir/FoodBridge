from helpers import *


def test(driver):
    fill_signup_form(driver, "No Address", "noaddress@gmail.com", "01711000009", "donor", "Banani", "", "pass1234", "pass1234")
    validation = get_validation_message(driver, "address")
    return validation != "" and "signup.html" in driver.current_url, "Browser message: " + validation


TEST_CASE = ("TC72", "Verify signup with an empty address",
             "Address: (empty), other fields valid", test)


def run():
    return run_test_module("Sign Up", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
