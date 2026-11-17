from helpers import *


def test(driver):
    open_page(driver, "forgot-password.html")
    type_text(driver, "email", COLLECTOR_EMAIL)
    type_text(driver, "phone", "0181100000")
    click(driver, "sendRequestBtn")
    validation = get_validation_message(driver, "phone")
    return validation != "" and "forgot-password.html" in driver.current_url, "Browser message: " + validation


TEST_CASE = ("TC107", "Verify a reset request cannot be sent with a 10 digit mobile number",
             "Email: collector@foodbridge.com, Mobile: 0181100000", test)


def run():
    return run_test_module("Forgot Password", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
