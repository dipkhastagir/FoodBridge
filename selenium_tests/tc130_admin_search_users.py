from helpers import *


def test(driver):
    open_admin_tab(driver, "tab-users", "usersBody")
    type_text(driver, "userSearch", "smile")
    wait_until(driver, lambda d: len(d.find_elements(By.CSS_SELECTOR, "#usersBody tr[id^='user-']")) == 1)
    rows = driver.find_elements(By.CSS_SELECTOR, "#usersBody tr[id^='user-']")
    return len(rows) == 1 and "Smile Foundation" in rows[0].text, "Rows shown: " + str(len(rows))


TEST_CASE = ("TC130", "Verify admin can search the user list",
             "Search: smile", test)


def run():
    return run_test_module("Admin", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
