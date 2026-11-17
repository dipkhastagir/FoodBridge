from helpers import *


def test(driver):
    login(driver, COLLECTOR_EMAIL, COLLECTOR_PASSWORD)
    wait_until_page_ready(driver, "searchBtn")
    type_text(driver, "claim-qty-1", "5")
    click(driver, "claim-1")
    wait_for_message(driver)

    logout(driver)
    open_admin_dashboard(driver)
    click(driver, "tab-activity")
    type_text(driver, "activitySearch", "Chicken Biryani")
    click(driver, "activityFilterBtn")
    wait_until(driver, lambda d: "Claimed food" in d.find_element(By.ID, "activityBody").text)
    first_row = driver.find_elements(By.CSS_SELECTOR, "#activityBody .activity-row")[0].text
    passed = "Hope Volunteers" in first_row and "Claimed food" in first_row and "5 servings of Chicken Biryani" in first_row
    return passed, "Newest matching log line: " + first_row.replace("\n", " | ")


TEST_CASE = ("TC50", "Verify the activity log records user actions",
             "Collector claims 5 Chicken Biryani, admin searches the log for Chicken Biryani", test)


def run():
    return run_test_module("Admin", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
