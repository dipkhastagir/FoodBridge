from helpers import *


def test(driver):
    login(driver, DONOR_EMAIL, DONOR_PASSWORD)
    open_profile(driver)
    type_text(driver, "profileName", "")
    click(driver, "saveProfileBtn")
    validation = get_validation_message(driver, "profileName")
    return validation != "", "Browser message: " + validation


TEST_CASE = ("TC81", "Verify the profile cannot be saved with an empty name",
             "Name: (empty)", test)


def run():
    return run_test_module("Profile", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
