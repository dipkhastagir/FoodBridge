from helpers import *


def test(driver):
    open_donor_dashboard(driver)
    fill_food_form(driver, "Cup Cakes", "Bakery", "0", "5", "Uttara Sector 7", "")
    validation = get_validation_message(driver, "quantity")
    return validation != "", "Browser message: " + validation


TEST_CASE = ("TC16", "Verify food post with quantity 0",
             "Food: Cup Cakes, Qty: 0", test)


def run():
    return run_test_module("Donor Dashboard", [TEST_CASE], login_as=(DONOR_EMAIL, DONOR_PASSWORD))


if __name__ == "__main__":
    run()
