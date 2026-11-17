from helpers import *


def test(driver):
    open_donor_dashboard(driver)
    fill_food_form(driver, "Hot Tea", "Drinks & Dairy", "10", "1", "Banani Road 11", "")
    message = wait_for_message(driver)
    return "added successfully" in message, message


TEST_CASE = ("TC85", "Verify food can be posted with the shortest fresh time of 1 hour",
             "Food: Hot Tea, Fresh for: 1 hour", test)


def run():
    return run_test_module("Donor Dashboard", [TEST_CASE], login_as=(DONOR_EMAIL, DONOR_PASSWORD))


if __name__ == "__main__":
    run()
