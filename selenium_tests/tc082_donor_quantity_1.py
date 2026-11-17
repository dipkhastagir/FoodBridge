from helpers import *


def test(driver):
    open_donor_dashboard(driver)
    fill_food_form(driver, "Single Samosa", "Dry Food", "1", "6", "Banani Road 11", "")
    message = wait_for_message(driver)
    return "added successfully" in message, message


TEST_CASE = ("TC82", "Verify food can be posted with the lowest quantity 1",
             "Food: Single Samosa, Quantity: 1", test)


def run():
    return run_test_module("Donor Dashboard", [TEST_CASE], login_as=(DONOR_EMAIL, DONOR_PASSWORD))


if __name__ == "__main__":
    run()
