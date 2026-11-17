from helpers import *


def test(driver):
    open_admin_tab(driver, "tab-claims", "claimsBody")
    click(driver, "addClaimBtn")
    choose_option(driver, "newClaimFood", "2")
    choose_option(driver, "newClaimCollector", "2")
    type_text(driver, "newClaimQuantity", "4")
    click(driver, "saveClaimBtn")
    message = wait_for_message(driver)
    click(driver, "tab-foods")
    servings = find(driver, "admin-food-2").find_element(By.CSS_SELECTOR, ".admin-servings").text
    passed = "4 servings of Fresh Bread Loaves were claimed for Hope Volunteers" in message and servings.startswith("11 left of 15")
    return passed, message + " | Fresh Bread Loaves now: " + servings.split("\n")[0]


TEST_CASE = ("TC59", "Verify admin can add a claim for a collector",
             "Food: Fresh Bread Loaves (15 left), Collector: Hope Volunteers, Servings: 4", test)


def run():
    return run_test_module("Admin", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
