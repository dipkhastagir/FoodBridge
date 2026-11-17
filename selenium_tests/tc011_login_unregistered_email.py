from helpers import *


def test(driver):
    fill_login_form(driver, "nobody@gmail.com", "donor123")
    message = wait_for_message(driver)
    return message == "Invalid email or password.", message


TEST_CASE = ("TC11", "Verify login with unregistered email",
             "Email: nobody@gmail.com, Password: donor123", test)


def run():
    return run_test_module("Login", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
