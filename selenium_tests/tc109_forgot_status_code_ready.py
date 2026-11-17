from helpers import *


def test(driver):
    send_request(driver, COLLECTOR_EMAIL, "01811000002", "")
    admin_give_code(driver, 1, "482913")
    open_page(driver, "reset-password.html?email=" + COLLECTOR_EMAIL)
    wait_until(driver, lambda d: "given you a code" in d.find_element(By.ID, "requestStatus").text)
    status = find(driver, "requestStatus").text
    return "given you a code" in status, "Status: " + status


TEST_CASE = ("TC109", "Verify the code page tells the user when the admin has given a code",
             "Request for collector@foodbridge.com, admin saves code 482913", test)


def run():
    return run_test_module("Forgot Password", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
