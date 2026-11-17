from helpers import *


def test(driver):
    send_request(driver, COLLECTOR_EMAIL, "01811000002", "")
    admin_give_code(driver, 1, "482913")
    open_page(driver, "reset-password.html?email=" + COLLECTOR_EMAIL)
    for wrong in ["000001", "000002", "000003", "000004", "000005"]:
        type_text(driver, "code", wrong)
        click(driver, "verifyCodeBtn")
        wait_for_message(driver)
    type_text(driver, "code", "482913")
    click(driver, "verifyCodeBtn")
    message = wait_for_message(driver)
    return message.startswith("Too many wrong codes"), "Right code after 5 wrong ones: " + message


TEST_CASE = ("TC113", "Verify after 5 wrong codes even the right code is refused",
             "Admin code: 482913, user types 5 wrong codes, then 482913", test)


def run():
    return run_test_module("Forgot Password", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
