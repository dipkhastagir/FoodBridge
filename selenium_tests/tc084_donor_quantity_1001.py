from helpers import *


def test(driver):
    open_donor_dashboard(driver)
    fill_food_form(driver, "Too Much Rice", "Cooked Meal", "1001", "6", "Banani Road 11", "")
    validation = get_validation_message(driver, "quantity")
    not_added = "Too Much Rice" not in find(driver, "foodTableBody").text
    return validation != "" and not_added, "Browser message: " + validation


TEST_CASE = ("TC84", "Verify food cannot be posted with quantity 1001",
             "Food: Too Much Rice, Quantity: 1001", test)


def run():
    return run_test_module("Donor Dashboard", [TEST_CASE], login_as=(DONOR_EMAIL, DONOR_PASSWORD))


if __name__ == "__main__":
    run()
