from helpers import *


def test(driver):
    fill_signup_form(driver, "Prefix Low", "prefix013@gmail.com", "01311223344", "collector", "Badda", "Road 2", "pass1234", "pass1234")
    message = wait_for_message(driver)
    return "successfully" in message, message


TEST_CASE = ("TC65", "Verify signup with the lowest valid mobile prefix 013",
             "Mobile: 01311223344", test)


def run():
    return run_test_module("Sign Up", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
