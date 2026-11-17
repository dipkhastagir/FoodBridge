from helpers import *


def test(driver):
    fill_signup_form(driver, "Sadia", "sadia@gmail.com", "01911223344", "collector", "Uttara", "Sector 4", "sadia123", "sadia999")
    message = wait_for_message(driver)
    return message == "Passwords do not match.", message


TEST_CASE = ("TC05", "Verify signup with mismatched passwords",
             "Password: sadia123, Confirm Password: sadia999", test)


def run():
    return run_test_module("Sign Up", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
