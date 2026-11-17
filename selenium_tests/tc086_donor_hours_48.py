from helpers import *


def test(driver):
    open_donor_dashboard(driver)
    fill_food_form(driver, "Dry Biscuits", "Dry Food", "10", "48", "Banani Road 11", "")
    message = wait_for_message(driver)
    return "added successfully" in message, message


TEST_CASE = ("TC86", "Verify food can be posted with the longest fresh time of 48 hours",
             "Food: Dry Biscuits, Fresh for: 48 hours", test)


def run():
    return run_test_module("Donor Dashboard", [TEST_CASE], login_as=(DONOR_EMAIL, DONOR_PASSWORD))


if __name__ == "__main__":
    run()
