from helpers import *


def test(driver):
    fill_signup_form(driver, "", "nameless@gmail.com", "01711000000", "donor", "Banani", "Road 11", "pass1234", "pass1234")
    validation = get_validation_message(driver, "name")
    still_on_page = "signup.html" in driver.current_url
    return validation != "" and still_on_page, "Browser message: " + validation


TEST_CASE = ("TC03", "Verify signup with empty Name field",
             "Name: (blank), Email: nameless@gmail.com, Password: pass1234", test)


def run():
    return run_test_module("Sign Up", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
