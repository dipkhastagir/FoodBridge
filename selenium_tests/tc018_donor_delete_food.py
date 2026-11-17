from helpers import *


def test(driver):
    open_donor_dashboard(driver)
    click(driver, "delete-3")
    accept_alert(driver)
    message = wait_for_message(driver)
    gone = not element_exists(driver, "food-3")
    return "deleted successfully" in message and gone, message + " | Removed from table: " + str(gone)


TEST_CASE = ("TC18", "Verify donor can delete a food post",
             "Delete 'Mixed Fruits Basket', click OK on confirm box", test)


def run():
    return run_test_module("Donor Dashboard", [TEST_CASE], login_as=(DONOR_EMAIL, DONOR_PASSWORD))


if __name__ == "__main__":
    run()
