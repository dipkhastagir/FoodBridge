from helpers import *


def test(driver):
    send_request(driver, COLLECTOR_EMAIL, "01811000002", "")
    admin_give_code(driver, 1, "482913")
    open_page(driver, "reset-password.html?email=" + COLLECTOR_EMAIL)
    type_text(driver, "code", "482913")
    click(driver, "verifyCodeBtn")
    wait_until_page_ready(driver, "passwordStep")
    type_text(driver, "newPassword", NEW_PASSWORD)
    type_text(driver, "confirmPassword", NEW_PASSWORD)
    click(driver, "savePasswordBtn")
    wait_until(driver, lambda d: "Password reset" in d.find_element(By.ID, "passwordMessage").text)
    open_page(driver, "reset-password.html?email=" + COLLECTOR_EMAIL)
    type_text(driver, "code", "482913")
    click(driver, "verifyCodeBtn")
    message = wait_for_message(driver)
    return "closed" in message, "Same code again: " + message


TEST_CASE = ("TC118", "Verify a reset code cannot be used a second time",
             "Admin code: 482913, reset the password, then try 482913 again", test)


def run():
    return run_test_module("Forgot Password", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
