from helpers import *


def test(driver):
    login(driver, DONOR_EMAIL, DONOR_PASSWORD)
    open_profile(driver)
    type_text(driver, "currentPassword", "wrongpass")
    type_text(driver, "newPassword", "newpass123")
    type_text(driver, "confirmNewPassword", "newpass123")
    click(driver, "changePasswordBtn")
    message = wait_for_message(driver, "passwordMessage")
    return message == "Current password is incorrect.", message


TEST_CASE = ("TC28", "Verify change password with wrong current password",
             "Current: wrongpass, New: newpass123, Confirm: newpass123", test)


def run():
    return run_test_module("Profile & Security", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
