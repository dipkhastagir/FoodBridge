from helpers import *


def test(driver):
    fill_signup_form(driver, "Prefix High", "prefix019@gmail.com", "01911223355", "donor", "Wari", "Road 9", "pass1234", "pass1234")
    message = wait_for_message(driver)
    return "successfully" in message, message


TEST_CASE = ("TC66", "Verify signup with the highest valid mobile prefix 019",
             "Mobile: 01911223355", test)


def run():
    return run_test_module("Sign Up", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
