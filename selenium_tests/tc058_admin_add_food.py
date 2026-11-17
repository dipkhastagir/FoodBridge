from helpers import *


def test(driver):
    open_admin_tab(driver, "tab-foods", "foodsBody")
    click(driver, "addFoodBtn")
    choose_option(driver, "editFoodDonor", "1")
    type_text(driver, "editFoodTitle", "Admin Pulao")
    choose_option(driver, "editFoodType", "Cooked Meal")
    type_text(driver, "editFoodQuantity", "15")
    click(driver, "saveFoodEditBtn")
    message = wait_for_message(driver)
    wait_until(driver, lambda d: "Admin Pulao" in d.find_element(By.ID, "foodsBody").text)
    passed = "was added for Dhaka Food Corner" in message
    return passed, message


TEST_CASE = ("TC58", "Verify admin can add a food post for a donor",
             "Donor: Dhaka Food Corner, Food: Admin Pulao, Type: Cooked Meal, Qty: 15", test)


def run():
    return run_test_module("Admin", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
