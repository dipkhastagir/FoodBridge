from helpers import *


def test(driver):
    open_donor_dashboard(driver)
    no_edit = not element_exists(driver, "edit-4")
    row = find(driver, "food-4").text
    return no_edit and "Confirm pickups above" in row, "Edit button shown: " + str(not no_edit) + " | Row says: Confirm pickups above"


TEST_CASE = ("TC91", "Verify a donor cannot edit food that a collector already claimed",
             "Food: Vegetable Khichuri (claimed by Hope Volunteers)", test)


def run():
    return run_test_module("Donor Dashboard", [TEST_CASE], login_as=(DONOR_EMAIL, DONOR_PASSWORD))


if __name__ == "__main__":
    run()
