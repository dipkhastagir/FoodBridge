from helpers import *


def test(driver):
    open_admin_tab(driver, "tab-users", "usersBody")
    click(driver, "addUserBtn")
    type_text(driver, "editUserName", "Short Pass")
    type_text(driver, "editUserEmail", "shortpass@gmail.com")
    type_text(driver, "editUserPhone", "01611223388")
    choose_option(driver, "editUserArea", "Badda")
    type_text(driver, "editUserAddress", "Road 1")
    choose_option(driver, "editUserRole", "donor")
    type_text(driver, "editUserPassword", "abc12")
    click(driver, "saveUserBtn")
    message = wait_for_message(driver, "userModalMessage")
    return "at least 6 characters" in message, message


TEST_CASE = ("TC122", "Verify admin cannot add a user with a 5 character password",
             "Name: Short Pass, Password: abc12", test)


def run():
    return run_test_module("Admin", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
