from helpers import *


def test(driver):
    send_request(driver, COLLECTOR_EMAIL, "01811000002", "")
    admin_give_code(driver, 1, "482913")
    send_request(driver, COLLECTOR_EMAIL, "01811000002", "Sending again")
    type_text(driver, "code", "482913")
    click(driver, "verifyCodeBtn")
    message = wait_for_message(driver)
    return "not given you a code yet" in message, "Old code after a new request: " + message


TEST_CASE = ("TC115", "Verify a new request makes the old code stop working",
             "Request 1 gets code 482913, user sends request 2, then tries 482913", test)


def run():
    return run_test_module("Forgot Password", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
