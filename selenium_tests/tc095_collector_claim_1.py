from helpers import *


def test(driver):
    open_collector_dashboard(driver)
    type_text(driver, "claim-qty-1", "1")
    click(driver, "claim-1")
    message = wait_for_message(driver)
    left = find(driver, "remaining-1").text
    return "You claimed 1 servings" in message and left == "19", message + " | Left: " + left


TEST_CASE = ("TC95", "Verify a collector can claim the lowest amount of 1 serving",
             "Food: Chicken Biryani (20 left), Quantity: 1", test)


def run():
    return run_test_module("Collector Dashboard", [TEST_CASE], login_as=(COLLECTOR_EMAIL, COLLECTOR_PASSWORD))


if __name__ == "__main__":
    run()
