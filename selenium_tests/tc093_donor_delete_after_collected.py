from helpers import *


def test(driver):
    open_donor_dashboard(driver)
    click(driver, "delete-5")
    accept_alert(driver)
    message = wait_for_message(driver)
    gone = not element_exists(driver, "food-5")
    return "deleted successfully" in message and gone, message + " | Removed: " + str(gone)


TEST_CASE = ("TC93", "Verify a donor can delete food after every pickup is confirmed",
             "Food: Egg Fried Rice (collected)", test)


def run():
    return run_test_module("Donor Dashboard", [TEST_CASE], login_as=(DONOR_EMAIL, DONOR_PASSWORD))


if __name__ == "__main__":
    run()
