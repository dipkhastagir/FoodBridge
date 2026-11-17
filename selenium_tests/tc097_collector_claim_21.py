from helpers import *


def test(driver):
    open_collector_dashboard(driver)
    type_text(driver, "claim-qty-1", "21")
    click(driver, "claim-1")
    validation = get_validation_message(driver, "claim-qty-1")
    left = find(driver, "remaining-1").text
    return validation != "" and left == "20", "Browser message: " + validation + " | Left: " + left


TEST_CASE = ("TC97", "Verify a collector cannot claim one more than what is left",
             "Food: Chicken Biryani (20 left), Quantity: 21", test)


def run():
    return run_test_module("Collector Dashboard", [TEST_CASE], login_as=(COLLECTOR_EMAIL, COLLECTOR_PASSWORD))


if __name__ == "__main__":
    run()
