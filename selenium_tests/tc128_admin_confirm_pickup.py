from helpers import *


def test(driver):
    open_admin_tab(driver, "tab-claims", "claimsBody")
    click(driver, "confirm-claim-1")
    message = wait_for_message(driver)
    wait_until(driver, lambda d: "Collected" in d.find_element(By.CSS_SELECTOR, "#admin-claim-1 .claim-status").text)
    return "Pickup confirmed" in message, message + " | Status: Collected"


TEST_CASE = ("TC128", "Verify admin can confirm a pickup from the Claims tab",
             "Claim: 25 servings of Vegetable Khichuri by Hope Volunteers", test)


def run():
    return run_test_module("Admin", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
