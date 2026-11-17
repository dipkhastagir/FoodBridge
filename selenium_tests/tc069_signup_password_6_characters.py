from helpers import *


def test(driver):
    fill_signup_form(driver, "Six Chars", "six@gmail.com", "01711000006", "collector", "Banani", "Road 11", "abc123", "abc123")
    message = wait_for_message(driver)
    return "successfully" in message, message


TEST_CASE = ("TC69", "Verify signup with a password of exactly 6 characters",
             "Password: abc123, Confirm Password: abc123", test)


def run():
    return run_test_module("Sign Up", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
