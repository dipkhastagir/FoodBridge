from helpers import *


def test(driver):
    open_admin_dashboard(driver)
    click(driver, "tab-foods")
    click(driver, "delete-food-3")
    accept_alert(driver)
    message = wait_for_message(driver)
    wait_until(driver, lambda d: not element_exists(d, "admin-food-3"))
    passed = "was deleted" in message and not element_exists(driver, "admin-food-3")
    return passed, message


TEST_CASE = ("TC51", "Verify admin can delete a food post",
             "Delete: Mixed Fruits Basket, click OK on confirm box", test)


def run():
    return run_test_module("Admin", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
