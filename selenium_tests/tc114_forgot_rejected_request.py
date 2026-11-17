from helpers import *


def test(driver):
    send_request(driver, COLLECTOR_EMAIL, "01811000002", "")
    logout(driver)
    open_admin_dashboard(driver)
    click(driver, "reject-1")
    accept_alert(driver)
    wait_for_message(driver)
    logout(driver)
    open_page(driver, "reset-password.html?email=" + COLLECTOR_EMAIL)
    type_text(driver, "code", "482913")
    click(driver, "verifyCodeBtn")
    message = wait_for_message(driver)
    return "rejected this request" in message, message


TEST_CASE = ("TC114", "Verify a user is told when the admin rejected the request",
             "Request for collector@foodbridge.com, admin clicks Reject, user enters 482913", test)


def run():
    return run_test_module("Forgot Password", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
