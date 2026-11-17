from helpers import *


def test(driver):
    fill_signup_form(driver, "   ", "spaces@gmail.com", "01711000000", "donor", "Banani", "Road 11", "pass1234", "pass1234")
    message = wait_for_message(driver)
    return message == "Name and address cannot be only spaces.", message


TEST_CASE = ("TC61", "Verify signup with a name made of only spaces",
             "Name: (3 spaces), Email: spaces@gmail.com, Mobile: 01711000000, Role: Donor, Area: Banani", test)


def run():
    return run_test_module("Sign Up", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
