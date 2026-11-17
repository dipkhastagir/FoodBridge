from helpers import *


def test(driver):
    open_collector_dashboard(driver)
    type_text(driver, "claim-qty-1", "20")
    click(driver, "claim-1")
    message = wait_for_message(driver)
    gone = not element_exists(driver, "food-card-1")
    return "last of it" in message and gone, message + " | Removed from list: " + str(gone)


TEST_CASE = ("TC96", "Verify a collector can claim every serving that is left",
             "Food: Chicken Biryani (20 left), Quantity: 20", test)


def run():
    return run_test_module("Collector Dashboard", [TEST_CASE], login_as=(COLLECTOR_EMAIL, COLLECTOR_PASSWORD))


if __name__ == "__main__":
    run()
