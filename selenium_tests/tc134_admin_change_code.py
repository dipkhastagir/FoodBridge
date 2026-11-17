from helpers import *


def test(driver):
    send_request(driver, COLLECTOR_EMAIL, "01811000002", "")
    admin_give_code(driver, 1, "111111")
    admin_give_code(driver, 1, "222222")
    open_page(driver, "reset-password.html?email=" + COLLECTOR_EMAIL)
    type_text(driver, "code", "111111")
    click(driver, "verifyCodeBtn")
    old_message = wait_for_message(driver)
    type_text(driver, "code", "222222")
    click(driver, "verifyCodeBtn")
    wait_until_page_ready(driver, "passwordStep")
    return old_message.startswith("Wrong code"), "First code: " + old_message + " | Second code accepted: True"


TEST_CASE = ("TC134", "Verify a changed code replaces the first code",
             "Admin saves 111111, then changes it to 222222, user tries both", test)


def run():
    return run_test_module("Admin", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
