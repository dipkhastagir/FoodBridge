from helpers import *


def test(driver):
    login(driver, DONOR_EMAIL, DONOR_PASSWORD)
    open_profile(driver)
    type_text(driver, "profilePhone", "0171122334")
    click(driver, "saveProfileBtn")
    validation = get_validation_message(driver, "profilePhone")
    return validation != "", "Browser message: " + validation


TEST_CASE = ("TC80", "Verify the profile cannot be saved with a 10 digit mobile number",
             "Mobile: 0171122334", test)


def run():
    return run_test_module("Profile", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
