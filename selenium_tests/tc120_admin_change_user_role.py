from helpers import *


def test(driver):
    open_admin_tab(driver, "tab-users", "usersBody")
    click(driver, "edit-user-3")
    choose_option(driver, "editUserRole", "donor")
    click(driver, "saveUserBtn")
    message = wait_for_message(driver)
    logout(driver)
    login(driver, COLLECTOR2_EMAIL, COLLECTOR2_PASSWORD)
    donor_page = wait_for_url(driver, "donor-dashboard.html")
    return "was updated" in message and donor_page, message + " | Smile Foundation now opens: " + driver.current_url


TEST_CASE = ("TC120", "Verify admin can change a user's role from Edit user",
             "User: Smile Foundation, Role: Collector changed to Donor", test)


def run():
    return run_test_module("Admin", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
