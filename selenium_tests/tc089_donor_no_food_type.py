from helpers import *


def test(driver):
    open_donor_dashboard(driver)
    fill_food_form(driver, "Mystery Box", "", "10", "6", "Banani Road 11", "")
    validation = get_validation_message(driver, "foodType")
    return validation != "", "Browser message: " + validation


TEST_CASE = ("TC89", "Verify food cannot be posted without a food type",
             "Food: Mystery Box, Type: (not selected)", test)


def run():
    return run_test_module("Donor Dashboard", [TEST_CASE], login_as=(DONOR_EMAIL, DONOR_PASSWORD))


if __name__ == "__main__":
    run()
