from helpers import *


def test(driver):
    login(driver, DONOR_EMAIL, DONOR_PASSWORD)
    wait_until_page_ready(driver, "switchRoleBtn")
    click(driver, "switchRoleBtn")
    accept_alert(driver)
    moved = wait_for_url(driver, "collector-dashboard.html")
    wait_until_page_ready(driver, "searchBtn")
    badge = find(driver, "navUserRole").text
    wait_until(driver, lambda d: d.find_element(By.ID, "emptyState").is_displayed())
    own_food_hidden = len(driver.find_elements(By.CSS_SELECTOR, "#foodGrid .food-card")) == 0
    passed = moved and badge == "Collector" and own_food_hidden
    return passed, f"Now on: {driver.current_url} | Badge: {badge} | Own food hidden: {own_food_hidden}"


TEST_CASE = ("TC37", "Verify donor can switch to collector role",
             "Login: donor@foodbridge.com, click Switch to Collector, click OK", test)


def run():
    return run_test_module("Role Switch", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
