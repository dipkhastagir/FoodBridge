from helpers import *


def test(driver):
    open_donor_dashboard(driver)
    fill_food_form(driver, "Plain Rice", "Cooked Meal", "10", "6", "", "")
    validation = get_validation_message(driver, "location")
    return validation != "", "Browser message: " + validation


TEST_CASE = ("TC90", "Verify food cannot be posted without a pickup address",
             "Food: Plain Rice, Pickup address: (empty)", test)


def run():
    return run_test_module("Donor Dashboard", [TEST_CASE], login_as=(DONOR_EMAIL, DONOR_PASSWORD))


if __name__ == "__main__":
    run()
