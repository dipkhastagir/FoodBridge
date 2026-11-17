from helpers import *


def test(driver):
    open_admin_tab(driver, "tab-foods", "foodsBody")
    click(driver, "edit-food-4")
    type_text(driver, "editFoodQuantity", "24")
    click(driver, "saveFoodEditBtn")
    validation = get_validation_message(driver, "editFoodQuantity")
    return validation != "", "Browser message: " + validation


TEST_CASE = ("TC124", "Verify admin cannot set a quantity below what collectors already took",
             "Food: Vegetable Khichuri (25 claimed), Total quantity: 24", test)


def run():
    return run_test_module("Admin", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
