from helpers import *


def test(driver):
    answer = send_request(driver, COLLECTOR_EMAIL, "01811000002", "Please call after 5 pm")
    on_code_page = "reset-password.html" in driver.current_url
    wait_until(driver, lambda d: d.find_element(By.ID, "requestStatus").text.strip() != "")
    status = find(driver, "requestStatus").text
    passed = "sent to the admin" in answer and on_code_page and "waiting for the admin" in status
    return passed, answer + " | Status on code page: " + status


TEST_CASE = ("TC39", "Verify user can send a password reset request to the admin",
             "Email: collector@foodbridge.com, Mobile: 01811000002, Message: Please call after 5 pm", test)


def run():
    return run_test_module("Forgot Password", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
