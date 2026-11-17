from helpers import *


def test(driver):
    fill_signup_form(driver, "Five Chars", "five@gmail.com", "01711000005", "donor", "Banani", "Road 11", "abc12", "abc12")
    message = wait_for_message(driver)
    return "at least 6 characters" in message, message


TEST_CASE = ("TC68", "Verify signup with a password of exactly 5 characters",
             "Password: abc12, Confirm Password: abc12", test)


def run():
    return run_test_module("Sign Up", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
