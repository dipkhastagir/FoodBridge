from helpers import *


def test(driver):
    open_donor_dashboard(driver)
    click(driver, "confirm-1")
    message = wait_for_message(driver)
    status = driver.find_element(By.CSS_SELECTOR, "#food-4 .status").text
    left_panel = not element_exists(driver, "confirm-item-1")
    passed = "Pickup confirmed" in message and status == "Collected" and left_panel
    return passed, message + " | Status: " + status + " | Removed from confirmation panel: " + str(left_panel)


TEST_CASE = ("TC19", "Verify donor can confirm pickup of claimed food",
             "Claim: Vegetable Khichuri, 25 servings by Hope Volunteers, click Confirm pickup", test)


def run():
    return run_test_module("Donor Dashboard", [TEST_CASE], login_as=(DONOR_EMAIL, DONOR_PASSWORD))


if __name__ == "__main__":
    run()
