from helpers import *


def test(driver):
    open_admin_tab(driver, "tab-claims", "claimsBody")
    click(driver, "addClaimBtn")
    choose_option(driver, "newClaimFood", "2")
    choose_option(driver, "newClaimCollector", "2")
    type_text(driver, "newClaimQuantity", "15")
    click(driver, "saveClaimBtn")
    message = wait_for_message(driver)
    click(driver, "tab-foods")
    servings = find(driver, "admin-food-2").find_element(By.CSS_SELECTOR, ".admin-servings").text
    return "15 servings" in message and servings.startswith("0 left of 15"), message + " | Servings: " + servings.split("\n")[0]


TEST_CASE = ("TC127", "Verify admin can add a claim for exactly what is left",
             "Food: Fresh Bread Loaves (15 left), Collector: Hope Volunteers, Servings: 15", test)


def run():
    return run_test_module("Admin", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
