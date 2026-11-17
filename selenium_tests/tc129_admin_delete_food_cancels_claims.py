from helpers import *


def test(driver):
    open_admin_tab(driver, "tab-foods", "foodsBody")
    click(driver, "delete-food-4")
    accept_alert(driver)
    message = wait_for_message(driver)
    click(driver, "tab-claims")
    claim_gone = not element_exists(driver, "admin-claim-1")
    return "was deleted" in message and claim_gone, message + " | Waiting claim removed: " + str(claim_gone)


TEST_CASE = ("TC129", "Verify deleting a food post also removes its waiting claims",
             "Food: Vegetable Khichuri (waiting claim of 25), click Delete, click OK", test)


def run():
    return run_test_module("Admin", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
