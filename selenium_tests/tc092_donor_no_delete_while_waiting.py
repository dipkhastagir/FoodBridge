from helpers import *


def test(driver):
    open_donor_dashboard(driver)
    no_delete = not element_exists(driver, "delete-4")
    return no_delete, "Delete button shown: " + str(not no_delete)


TEST_CASE = ("TC92", "Verify a donor cannot delete food while a pickup is waiting",
             "Food: Vegetable Khichuri (pickup waiting)", test)


def run():
    return run_test_module("Donor Dashboard", [TEST_CASE], login_as=(DONOR_EMAIL, DONOR_PASSWORD))


if __name__ == "__main__":
    run()
