from helpers import *


def test(driver):
    login(driver, DONOR_EMAIL, DONOR_PASSWORD)
    open_profile(driver)
    type_text(driver, "currentPassword", DONOR_PASSWORD)
    type_text(driver, "newPassword", "abc12")
    type_text(driver, "confirmNewPassword", "abc12")
    click(driver, "changePasswordBtn")
    message = wait_for_message(driver, "passwordMessage")
    return "at least 6 characters" in message, message


TEST_CASE = ("TC76", "Verify a new password of exactly 5 characters is refused",
             "Current: Donor@FoodBridge26, New: abc12, Confirm: abc12", test)


def run():
    return run_test_module("Profile", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
