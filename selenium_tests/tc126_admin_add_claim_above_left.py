from helpers import *


def test(driver):
    open_admin_tab(driver, "tab-claims", "claimsBody")
    click(driver, "addClaimBtn")
    choose_option(driver, "newClaimFood", "2")
    choose_option(driver, "newClaimCollector", "2")
    type_text(driver, "newClaimQuantity", "16")
    click(driver, "saveClaimBtn")
    validation = get_validation_message(driver, "newClaimQuantity")
    return validation != "", "Browser message: " + validation


TEST_CASE = ("TC126", "Verify admin cannot add a claim larger than what is left",
             "Food: Fresh Bread Loaves (15 left), Collector: Hope Volunteers, Servings: 16", test)


def run():
    return run_test_module("Admin", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
