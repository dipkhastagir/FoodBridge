from helpers import *


def test(driver):
    open_collector_dashboard(driver)
    type_text(driver, "claim-qty-1", "0")
    click(driver, "claim-1")
    validation = get_validation_message(driver, "claim-qty-1")
    return validation != "", "Browser message: " + validation


TEST_CASE = ("TC98", "Verify a collector cannot claim 0 servings",
             "Food: Chicken Biryani, Quantity: 0", test)


def run():
    return run_test_module("Collector Dashboard", [TEST_CASE], login_as=(COLLECTOR_EMAIL, COLLECTOR_PASSWORD))


if __name__ == "__main__":
    run()
