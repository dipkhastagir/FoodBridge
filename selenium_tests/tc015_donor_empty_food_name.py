from helpers import *


def test(driver):
    open_donor_dashboard(driver)
    fill_food_form(driver, "", "Bakery", "10", "5", "Uttara Sector 7", "")
    validation = get_validation_message(driver, "foodTitle")
    return validation != "", "Browser message: " + validation


TEST_CASE = ("TC15", "Verify food post with empty Food name",
             "Food: (blank), Type: Bakery, Qty: 10, Fresh for: 5h, Location: Uttara Sector 7", test)


def run():
    return run_test_module("Donor Dashboard", [TEST_CASE], login_as=(DONOR_EMAIL, DONOR_PASSWORD))


if __name__ == "__main__":
    run()
