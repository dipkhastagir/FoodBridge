from helpers import *


def test(driver):
    open_admin_tab(driver, "tab-users", "usersBody")
    click(driver, "block-3")
    accept_alert(driver)
    wait_until(driver, lambda d: "Blocked" in d.find_element(By.CSS_SELECTOR, "#user-3 .user-status").text)
    click(driver, "block-3")
    accept_alert(driver)
    wait_until(driver, lambda d: "Active" in d.find_element(By.CSS_SELECTOR, "#user-3 .user-status").text)
    message = find(driver, "message").text
    logout(driver)
    login(driver, COLLECTOR2_EMAIL, COLLECTOR2_PASSWORD)
    logged_in = wait_for_url(driver, "collector-dashboard.html")
    return "unblocked" in message and logged_in, message + " | Smile Foundation logged in: " + str(logged_in)


TEST_CASE = ("TC119", "Verify admin can unblock a user and they can log in again",
             "User: Smile Foundation, click Block, then Unblock", test)


def run():
    return run_test_module("Admin", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
