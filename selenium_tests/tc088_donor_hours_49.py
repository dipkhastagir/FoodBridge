from helpers import *


def test(driver):
    open_donor_dashboard(driver)
    fill_food_form(driver, "Long Rice", "Cooked Meal", "10", "49", "Banani Road 11", "")
    validation = get_validation_message(driver, "expiryHours")
    return validation != "", "Browser message: " + validation


TEST_CASE = ("TC88", "Verify food cannot be posted with a fresh time of 49 hours",
             "Food: Long Rice, Fresh for: 49", test)


def run():
    return run_test_module("Donor Dashboard", [TEST_CASE], login_as=(DONOR_EMAIL, DONOR_PASSWORD))


if __name__ == "__main__":
    run()
