from helpers import *


def test(driver):
    login(driver, DONOR_EMAIL, DONOR_PASSWORD)
    open_profile(driver)
    type_text(driver, "profileName", "Dhaka Food Corner Ltd")
    type_text(driver, "profilePhone", "01700000099")
    click(driver, "saveProfileBtn")
    message = wait_for_message(driver, "profileMessage")

    open_profile(driver)
    saved_name = find(driver, "profileName").get_attribute("value")
    saved_phone = find(driver, "profilePhone").get_attribute("value")
    passed = "updated successfully" in message and saved_name == "Dhaka Food Corner Ltd" and saved_phone == "01700000099"
    return passed, f"{message} | After reload: {saved_name}, {saved_phone}"


TEST_CASE = ("TC27", "Verify user can update profile information",
             "Name: Dhaka Food Corner Ltd, Phone: 01700000099", test)


def run():
    return run_test_module("Profile & Security", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
