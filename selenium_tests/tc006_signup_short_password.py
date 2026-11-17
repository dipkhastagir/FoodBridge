from helpers import *


def test(driver):
    fill_signup_form(driver, "Nabil", "nabil@gmail.com", "01511223344", "donor", "Gulshan", "Road 90", "abc", "abc")
    message = wait_for_message(driver)
    return "at least 6 characters" in message, message


TEST_CASE = ("TC06", "Verify signup with a password shorter than 6 characters",
             "Password: abc, Confirm Password: abc", test)


def run():
    return run_test_module("Sign Up", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
