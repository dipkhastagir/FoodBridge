from helpers import *


def test(driver):
    send_request(driver, COLLECTOR_EMAIL, "01811000002", "")
    admin_give_code(driver, 1, "482913")
    open_page(driver, "reset-password.html?email=" + COLLECTOR_EMAIL)
    type_text(driver, "code", "482913")
    click(driver, "verifyCodeBtn")
    wait_until_page_ready(driver, "passwordStep")
    type_text(driver, "newPassword", "abc12")
    type_text(driver, "confirmPassword", "abc12")
    click(driver, "savePasswordBtn")
    wait_until(driver, lambda d: "at least 6" in d.find_element(By.ID, "passwordMessage").text)
    message = find(driver, "passwordMessage").text
    return "at least 6 characters" in message, message


TEST_CASE = ("TC116", "Verify the new password after reset must have at least 6 characters",
             "Admin code: 482913, New password: abc12", test)


def run():
    return run_test_module("Forgot Password", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
