from helpers import *


def test(driver):
    login(driver, DONOR_EMAIL, DONOR_PASSWORD)
    open_profile(driver)
    type_text(driver, "currentPassword", DONOR_PASSWORD)
    type_text(driver, "newPassword", "abc123")
    type_text(driver, "confirmNewPassword", "abc123")
    click(driver, "changePasswordBtn")
    message = wait_for_message(driver, "passwordMessage")
    return "changed successfully" in message, message


TEST_CASE = ("TC77", "Verify a new password of exactly 6 characters is accepted",
             "Current: Donor@FoodBridge26, New: abc123, Confirm: abc123", test)


def run():
    return run_test_module("Profile", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
