from helpers import *


def test(driver):
    open_collector_dashboard(driver)
    type_text(driver, "claim-qty-1", "5")
    click(driver, "claim-1")
    message = wait_for_message(driver)
    left = find(driver, "remaining-1").text
    passed = "You claimed 5 servings" in message and left == "15"
    return passed, message + " | Servings left on the ticket: " + left


TEST_CASE = ("TC24", "Verify collector can claim part of a food post",
             "Food: Chicken Biryani (20 servings), Quantity: 5", test)


def run():
    return run_test_module("Collector Dashboard", [TEST_CASE], login_as=(COLLECTOR_EMAIL, COLLECTOR_PASSWORD))


if __name__ == "__main__":
    run()
