from helpers import *


def test(driver):
    send_request(driver, COLLECTOR_EMAIL, "01811000002", "")
    admin_give_code(driver, 1, "731205")

    open_page(driver, "forgot-password.html")
    click(driver, "haveCodeLink")
    wait_for_url(driver, "reset-password.html")
    type_text(driver, "resetEmail", COLLECTOR_EMAIL)
    type_text(driver, "code", "000000")
    click(driver, "verifyCodeBtn")
    wrong_message = wait_for_message(driver)

    type_text(driver, "code", "731205")
    click(driver, "verifyCodeBtn")
    wait_until_page_ready(driver, "passwordStep")
    type_text(driver, "newPassword", NEW_PASSWORD)
    type_text(driver, "confirmPassword", NEW_PASSWORD)
    click(driver, "savePasswordBtn")
    wait_until(driver, lambda d: "Password reset" in d.find_element(By.ID, "passwordMessage").text)
    reset_message = find(driver, "passwordMessage").text

    login(driver, COLLECTOR_EMAIL, NEW_PASSWORD)
    logged_in = wait_for_url(driver, "collector-dashboard.html")
    passed = wrong_message.startswith("Wrong code") and "Password reset successfully" in reset_message and logged_in
    return passed, f"Wrong code: {wrong_message} | {reset_message} | Login with new password: {logged_in}"


TEST_CASE = ("TC41", "Verify password reset with the admin's code from 'Already have a code?'",
             "Admin code: 731205, user clicks 'Enter it here', Code: 000000 then 731205, New password: Fresh#Start2026", test)


def run():
    return run_test_module("Forgot Password", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
