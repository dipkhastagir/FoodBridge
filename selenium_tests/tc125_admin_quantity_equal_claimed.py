from helpers import *


def test(driver):
    open_admin_tab(driver, "tab-foods", "foodsBody")
    click(driver, "edit-food-4")
    type_text(driver, "editFoodQuantity", "25")
    click(driver, "saveFoodEditBtn")
    message = wait_for_message(driver)
    servings = find(driver, "admin-food-4").find_element(By.CSS_SELECTOR, ".admin-servings").text
    return "was updated" in message and servings.startswith("0 left of 25"), message + " | Servings: " + servings.split("\n")[0]


TEST_CASE = ("TC125", "Verify admin can set the quantity equal to what collectors already took",
             "Food: Vegetable Khichuri (25 claimed), Total quantity: 25", test)


def run():
    return run_test_module("Admin", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
