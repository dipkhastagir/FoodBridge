from helpers import *


def test(driver):
    open_admin_tab(driver, "tab-foods", "foodsBody")
    click(driver, "edit-food-1")
    type_text(driver, "editFoodQuantity", "30")
    click(driver, "saveFoodEditBtn")
    message = wait_for_message(driver)
    wait_until(driver, lambda d: "of 30" in d.find_element(By.CSS_SELECTOR, "#admin-food-1 .admin-servings").text)
    servings = find(driver, "admin-food-1").find_element(By.CSS_SELECTOR, ".admin-servings").text
    return "was updated" in message and "left of 30" in servings, message + " | Servings: " + servings


TEST_CASE = ("TC55", "Verify admin can change the quantity of a food post",
             "Food: Chicken Biryani, Total quantity: 20 -> 30", test)


def run():
    return run_test_module("Admin", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
