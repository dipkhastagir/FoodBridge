from helpers import *


def test(driver):
    open_admin_tab(driver, "tab-users", "usersBody")
    click(driver, "addUserBtn")
    type_text(driver, "editUserName", "Kuril Food Corner")
    type_text(driver, "editUserEmail", "kuril.food@gmail.com")
    type_text(driver, "editUserPhone", "01611223344")
    choose_option(driver, "editUserArea", "Kuril")
    type_text(driver, "editUserAddress", "Road 3, Kuril")
    choose_option(driver, "editUserRole", "donor")
    type_text(driver, "editUserPassword", "Kuril#Food2026")
    click(driver, "saveUserBtn")
    message = wait_for_message(driver)
    wait_until(driver, lambda d: "kuril.food@gmail.com" in d.find_element(By.ID, "usersBody").text)

    logout(driver)
    login(driver, "kuril.food@gmail.com", "Kuril#Food2026")
    logged_in = wait_for_url(driver, "donor-dashboard.html")
    passed = "was added as a donor" in message and logged_in
    return passed, message + " | New user logged in: " + str(logged_in)


TEST_CASE = ("TC57", "Verify admin can add a new user",
             "Name: Kuril Food Corner, Email: kuril.food@gmail.com, Mobile: 01611223344, Area: Kuril, Role: Donor, Password: Kuril#Food2026", test)


def run():
    return run_test_module("Admin", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
