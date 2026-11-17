from helpers import *


def test(driver):
    open_donor_dashboard(driver)
    click(driver, "edit-2")
    type_text(driver, "quantity", "25")
    click(driver, "saveFoodBtn")
    message = wait_for_message(driver)
    new_qty = driver.find_element(By.CSS_SELECTOR, "#food-2 .food-qty").text
    return "updated successfully" in message and new_qty == "25", message + " | New quantity: " + new_qty


TEST_CASE = ("TC17", "Verify donor can edit a food post",
             "Edit 'Fresh Bread Loaves': Qty 15 -> 25", test)


def run():
    return run_test_module("Donor Dashboard", [TEST_CASE], login_as=(DONOR_EMAIL, DONOR_PASSWORD))


if __name__ == "__main__":
    run()
