from helpers import *


def test(driver):
    open_admin_tab(driver, "tab-users", "usersBody")
    click(driver, "edit-user-2")
    type_text(driver, "editUserPassword", "Admin#Gave2026")
    click(driver, "saveUserBtn")
    message = wait_for_message(driver)

    logout(driver)
    login(driver, COLLECTOR_EMAIL, "Admin#Gave2026")
    logged_in = wait_for_url(driver, "collector-dashboard.html")
    return "was updated" in message and logged_in, message + " | Collector logged in with the new password: " + str(logged_in)


TEST_CASE = ("TC54", "Verify admin can set a new password for a user",
             "User: Hope Volunteers, New password: Admin#Gave2026, then log in", test)


def run():
    return run_test_module("Admin", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
