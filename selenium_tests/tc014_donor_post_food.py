from helpers import *


def test(driver):
    open_donor_dashboard(driver)
    fill_food_form(driver, "Beef Tehari", "Cooked Meal", "30", "6", "Mohakhali DOHS", "Packed in 30 boxes")
    message = wait_for_message(driver)
    in_table = "Beef Tehari" in find(driver, "foodTableBody").text
    return "added successfully" in message and in_table, message + " | Shown in My food posts: " + str(in_table)


TEST_CASE = ("TC14", "Verify donor can post food with valid information",
             "Food: Beef Tehari, Type: Cooked Meal, Qty: 30, Fresh for: 6h, Location: Mohakhali DOHS", test)


def run():
    return run_test_module("Donor Dashboard", [TEST_CASE], login_as=(DONOR_EMAIL, DONOR_PASSWORD))


if __name__ == "__main__":
    run()
