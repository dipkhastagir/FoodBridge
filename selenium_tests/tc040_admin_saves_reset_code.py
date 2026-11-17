from helpers import *


def test(driver):
    send_request(driver, COLLECTOR_EMAIL, "01811000002", "Please call after 5 pm")
    logout(driver)
    login(driver, ADMIN_EMAIL, ADMIN_PASSWORD)
    wait_until_page_ready(driver, "requestsBody")
    row = find(driver, "request-1").text
    type_text(driver, "code-input-1", "482913")
    click(driver, "save-code-1")
    message = wait_for_message(driver)
    wait_until(driver, lambda d: element_exists(d, "code-note-1"))
    passed = ("Hope Volunteers" in row and "Matches the account" in row
              and "482913 saved" in message and "2 hours" in message)
    return passed, f"Mobile matches: {'Matches the account' in row} | {message}"


TEST_CASE = ("TC40", "Verify admin can type and save a reset code",
             "Request from collector@foodbridge.com (01811000002), admin types Code: 482913, clicks Save code", test)


def run():
    return run_test_module("Forgot Password", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
