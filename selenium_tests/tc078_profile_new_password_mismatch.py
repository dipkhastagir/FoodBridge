from helpers import *


def test(driver):
    login(driver, DONOR_EMAIL, DONOR_PASSWORD)
    open_profile(driver)
    type_text(driver, "currentPassword", DONOR_PASSWORD)
    type_text(driver, "newPassword", "newpass123")
    type_text(driver, "confirmNewPassword", "newpass999")
    click(driver, "changePasswordBtn")
    message = wait_for_message(driver, "passwordMessage")
    return message == "New passwords do not match.", message


TEST_CASE = ("TC78", "Verify new passwords that do not match are refused",
             "New: newpass123, Confirm: newpass999", test)


def run():
    return run_test_module("Profile", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
