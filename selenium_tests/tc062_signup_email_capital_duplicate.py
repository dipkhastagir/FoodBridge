from helpers import *


def test(driver):
    fill_signup_form(driver, "Copy Cat", "DONOR@FOODBRIDGE.COM", "01611223344", "donor", "Banani", "Road 11", "copy1234", "copy1234")
    message = wait_for_message(driver)
    return "already registered" in message, message


TEST_CASE = ("TC62", "Verify signup with an existing email typed in capital letters",
             "Email: DONOR@FOODBRIDGE.COM (same as donor@foodbridge.com)", test)


def run():
    return run_test_module("Sign Up", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
