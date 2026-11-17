from helpers import *


def test(driver):
    open_admin_tab(driver, "tab-activity", "activityBody")
    choose_option(driver, "activityUser", "2")
    click(driver, "activityFilterBtn")
    wait_until(driver, lambda d: all("Hope Volunteers" in r.text for r in d.find_elements(By.CSS_SELECTOR, "#activityBody .activity-row")))
    rows = driver.find_elements(By.CSS_SELECTOR, "#activityBody .activity-row")
    return len(rows) > 0 and all("Hope Volunteers" in r.text for r in rows), "Rows shown: " + str(len(rows)) + ", all by Hope Volunteers"


TEST_CASE = ("TC132", "Verify admin can see the activity of one user only",
             "Activity log, User: Hope Volunteers", test)


def run():
    return run_test_module("Admin", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
