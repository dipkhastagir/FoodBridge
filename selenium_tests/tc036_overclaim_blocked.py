from helpers import *


def test(driver):
    login(driver, COLLECTOR_EMAIL, COLLECTOR_PASSWORD)
    open_collector_dashboard(driver)
    type_text(driver, "claim-qty-1", "50")
    click(driver, "claim-1")
    validation = get_validation_message(driver, "claim-qty-1")
    still_20 = find(driver, "remaining-1").text == "20"
    return validation != "" and still_20, "Browser message: " + validation + " | Servings left still 20: " + str(still_20)


TEST_CASE = ("TC36", "Verify collector cannot claim more servings than are left",
             "Food: Chicken Biryani (20 left), Quantity: 50", test)


def run():
    return run_test_module("Partial Claim", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
