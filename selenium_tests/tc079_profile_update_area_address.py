from helpers import *


def test(driver):
    login(driver, DONOR_EMAIL, DONOR_PASSWORD)
    open_profile(driver)
    wait_until(driver, lambda d: len(d.find_elements(By.CSS_SELECTOR, "#profileArea option")) > 1)
    choose_option(driver, "profileArea", "Gulshan")
    type_text(driver, "profileAddress", "Road 90, Gulshan 2")
    click(driver, "saveProfileBtn")
    message = wait_for_message(driver, "profileMessage")
    open_profile(driver)
    wait_until(driver, lambda d: d.find_element(By.ID, "profileArea").get_attribute("value") != "")
    area = find(driver, "profileArea").get_attribute("value")
    address = find(driver, "profileAddress").get_attribute("value")
    passed = "updated successfully" in message and area == "Gulshan" and address == "Road 90, Gulshan 2"
    return passed, message + " | After reload: " + area + ", " + address


TEST_CASE = ("TC79", "Verify a user can change the area and address and the change is saved",
             "Area: Gulshan, Address: Road 90, Gulshan 2", test)


def run():
    return run_test_module("Profile", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
