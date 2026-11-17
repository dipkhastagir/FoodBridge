from helpers import *


def test(driver):
    open_donor_dashboard(driver)
    fill_food_form(driver, "Wedding Rice", "Cooked Meal", "1000", "6", "Banani Road 11", "")
    message = wait_for_message(driver)
    return "added successfully" in message, message


TEST_CASE = ("TC83", "Verify food can be posted with the highest quantity 1000",
             "Food: Wedding Rice, Quantity: 1000", test)


def run():
    return run_test_module("Donor Dashboard", [TEST_CASE], login_as=(DONOR_EMAIL, DONOR_PASSWORD))


if __name__ == "__main__":
    run()
