from helpers import *


def test(driver):
    open_admin_tab(driver, "tab-claims", "claimsBody")
    click(driver, "cancel-claim-1")
    accept_alert(driver)
    message = wait_for_message(driver)
    wait_until(driver, lambda d: not element_exists(d, "admin-claim-1"))
    click(driver, "tab-foods")
    servings = find(driver, "admin-food-4").find_element(By.CSS_SELECTOR, ".admin-servings").text
    passed = "Claim cancelled" in message and servings.startswith("25 left of 25")
    return passed, message + " | Vegetable Khichuri now: " + servings.split("\n")[0]


TEST_CASE = ("TC56", "Verify admin can cancel a claim",
             "Claim: 25 servings of Vegetable Khichuri by Hope Volunteers", test)


def run():
    return run_test_module("Admin", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
