from helpers import *


def test(driver):
    open_page(driver, "reset-password.html?email=" + COLLECTOR_EMAIL)
    type_text(driver, "code", "12345")
    click(driver, "verifyCodeBtn")
    validation = get_validation_message(driver, "code")
    return validation != "", "Browser message: " + validation


TEST_CASE = ("TC110", "Verify the user cannot enter a code of only 5 digits",
             "Code: 12345", test)


def run():
    return run_test_module("Forgot Password", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
