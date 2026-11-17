from helpers import *


def test(driver):
    fill_signup_form(driver, "Copy Cat", "donor@foodbridge.com", "01611223344", "donor", "Banani", "Road 11", "copy1234", "copy1234")
    message = wait_for_message(driver)
    return "already registered" in message, message


TEST_CASE = ("TC07", "Verify signup with an already registered email",
             "Email: donor@foodbridge.com (already exists)", test)


def run():
    return run_test_module("Sign Up", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
