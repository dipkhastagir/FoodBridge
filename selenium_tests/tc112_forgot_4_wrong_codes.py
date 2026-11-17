from helpers import *


def test(driver):
    send_request(driver, COLLECTOR_EMAIL, "01811000002", "")
    admin_give_code(driver, 1, "482913")
    open_page(driver, "reset-password.html?email=" + COLLECTOR_EMAIL)
    message = ""
    for wrong in ["000001", "000002", "000003", "000004"]:
        type_text(driver, "code", wrong)
        click(driver, "verifyCodeBtn")
        message = wait_for_message(driver)
    return message == "Wrong code. You have 1 tries left.", "After 4 wrong codes: " + message


TEST_CASE = ("TC112", "Verify 4 wrong codes leave exactly 1 try",
             "Admin code: 482913, user types 000001 to 000004", test)


def run():
    return run_test_module("Forgot Password", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
