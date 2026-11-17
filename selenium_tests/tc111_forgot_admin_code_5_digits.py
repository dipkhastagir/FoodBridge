from helpers import *


def test(driver):
    send_request(driver, COLLECTOR_EMAIL, "01811000002", "")
    logout(driver)
    open_admin_dashboard(driver)
    type_text(driver, "code-input-1", "12345")
    click(driver, "save-code-1")
    message = wait_for_message(driver)
    return message == "Please type exactly 6 digits for the code.", message


TEST_CASE = ("TC111", "Verify the admin cannot save a code of only 5 digits",
             "Request for collector@foodbridge.com, admin types Code: 12345", test)


def run():
    return run_test_module("Forgot Password", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
