from helpers import *


def test(driver):
    login(driver, COLLECTOR_EMAIL, COLLECTOR_PASSWORD)
    wait_until_page_ready(driver, "switchRoleBtn")
    click(driver, "switchRoleBtn")
    accept_alert(driver)
    moved = wait_for_url(driver, "donor-dashboard.html")
    wait_until_page_ready(driver, "foodForm")
    type_text(driver, "foodTitle", "Extra Khichuri")
    choose_option(driver, "foodType", "Cooked Meal")
    type_text(driver, "quantity", "10")
    type_text(driver, "expiryHours", "3")
    type_text(driver, "location", "Mirpur 10")
    click(driver, "saveFoodBtn")
    message = wait_for_message(driver)
    badge = find(driver, "navUserRole").text
    passed = moved and badge == "Donor" and "added successfully" in message
    return passed, f"Now on: {driver.current_url} | Badge: {badge} | {message}"


TEST_CASE = ("TC38", "Verify collector can switch to donor role and post food",
             "Login: collector@foodbridge.com, Switch to Donor, Food: Extra Khichuri, Qty: 10", test)


def run():
    return run_test_module("Role Switch", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
