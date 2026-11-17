from helpers import *


def test(driver):
    open_admin_tab(driver, "tab-users", "usersBody")
    choose_option(driver, "userRoleFilter", "collector")
    wait_until(driver, lambda d: not element_exists(d, "user-1"))
    rows = driver.find_elements(By.CSS_SELECTOR, "#usersBody tr[id^='user-']")
    all_collectors = all("collector" in r.text.lower() for r in rows)
    return len(rows) == 2 and all_collectors, "Rows shown: " + str(len(rows)) + " | All collectors: " + str(all_collectors)


TEST_CASE = ("TC131", "Verify admin can show only collectors in the user list",
             "Role filter: Collectors", test)


def run():
    return run_test_module("Admin", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
