from helpers import *


def test(driver):
    open_admin_tab(driver, "tab-users", "usersBody")
    click(driver, "addUserBtn")
    type_text(driver, "editUserName", "Bad Mobile")
    type_text(driver, "editUserEmail", "badmobile@gmail.com")
    type_text(driver, "editUserPhone", "0161122338")
    choose_option(driver, "editUserArea", "Badda")
    type_text(driver, "editUserAddress", "Road 1")
    type_text(driver, "editUserPassword", "Good#2026")
    click(driver, "saveUserBtn")
    validation = get_validation_message(driver, "editUserPhone")
    return validation != "", "Browser message: " + validation


TEST_CASE = ("TC123", "Verify admin cannot add a user with a 10 digit mobile number",
             "Mobile: 0161122338", test)


def run():
    return run_test_module("Admin", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
