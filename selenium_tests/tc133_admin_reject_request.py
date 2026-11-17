from helpers import *


def test(driver):
    send_request(driver, COLLECTOR_EMAIL, "01811000002", "")
    logout(driver)
    open_admin_dashboard(driver)
    click(driver, "reject-1")
    accept_alert(driver)
    message = wait_for_message(driver)
    wait_until(driver, lambda d: "Rejected" in d.find_element(By.ID, "request-1").text)
    return message == "Request rejected.", message + " | Status: Rejected"


TEST_CASE = ("TC133", "Verify admin can reject a password reset request",
             "Request for collector@foodbridge.com, click Reject, click OK", test)


def run():
    return run_test_module("Admin", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
