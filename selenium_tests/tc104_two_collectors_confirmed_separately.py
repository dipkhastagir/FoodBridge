from helpers import *


def test(driver):
    login(driver, COLLECTOR_EMAIL, COLLECTOR_PASSWORD)
    open_collector_dashboard(driver)
    type_text(driver, "claim-qty-2", "5")
    click(driver, "claim-2")
    wait_for_message(driver)
    logout(driver)
    login(driver, COLLECTOR2_EMAIL, COLLECTOR2_PASSWORD)
    open_collector_dashboard(driver)
    type_text(driver, "claim-qty-2", "3")
    click(driver, "claim-2")
    wait_for_message(driver)
    logout(driver)
    login(driver, DONOR_EMAIL, DONOR_PASSWORD)
    wait_until_page_ready(driver, "confirmPanel")
    both = element_exists(driver, "confirm-item-3") and element_exists(driver, "confirm-item-4")
    click(driver, "confirm-3")
    wait_for_message(driver)
    wait_until(driver, lambda d: not element_exists(d, "confirm-item-3"))
    still_waiting = element_exists(driver, "confirm-item-4")
    return both and still_waiting, "Both claims shown: " + str(both) + " | After confirming Hope, Smile still waiting: " + str(still_waiting)


TEST_CASE = ("TC104", "Verify claims from two collectors on one post are confirmed separately",
             "Hope Volunteers claims 5 and Smile Foundation claims 3 of Fresh Bread Loaves, donor confirms only Hope", test)


def run():
    return run_test_module("Pickup Confirmation", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
