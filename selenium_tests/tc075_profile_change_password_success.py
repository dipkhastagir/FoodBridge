from helpers import *


def test(driver):
    login(driver, DONOR_EMAIL, DONOR_PASSWORD)
    open_profile(driver)
    type_text(driver, "currentPassword", DONOR_PASSWORD)
    type_text(driver, "newPassword", "Better#Pass26")
    type_text(driver, "confirmNewPassword", "Better#Pass26")
    click(driver, "changePasswordBtn")
    message = wait_for_message(driver, "passwordMessage")
    logout(driver)
    login(driver, DONOR_EMAIL, "Better#Pass26")
    logged_in = wait_for_url(driver, "donor-dashboard.html")
    return "changed successfully" in message and logged_in, message + " | Login with new password: " + str(logged_in)


TEST_CASE = ("TC75", "Verify a user can change the password and log in with the new one",
             "Current: Donor@FoodBridge26, New: Better#Pass26", test)


def run():
    return run_test_module("Profile", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
