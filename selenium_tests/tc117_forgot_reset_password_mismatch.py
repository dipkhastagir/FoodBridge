from helpers import *


def test(driver):
    send_request(driver, COLLECTOR_EMAIL, "01811000002", "")
    admin_give_code(driver, 1, "482913")
    open_page(driver, "reset-password.html?email=" + COLLECTOR_EMAIL)
    type_text(driver, "code", "482913")
    click(driver, "verifyCodeBtn")
    wait_until_page_ready(driver, "passwordStep")
    type_text(driver, "newPassword", "Fresh#Start2026")
    type_text(driver, "confirmPassword", "Fresh#Start2027")
    click(driver, "savePasswordBtn")
    wait_until(driver, lambda d: "do not match" in d.find_element(By.ID, "passwordMessage").text)
    message = find(driver, "passwordMessage").text
    return message == "Passwords do not match.", message


TEST_CASE = ("TC117", "Verify the two new passwords after reset must match",
             "Admin code: 482913, New: Fresh#Start2026, Confirm: Fresh#Start2027", test)


def run():
    return run_test_module("Forgot Password", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
