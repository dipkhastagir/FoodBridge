from helpers import *


def test(driver):
    open_admin_tab(driver, "tab-users", "usersBody")
    click(driver, "addUserBtn")
    type_text(driver, "editUserName", "Second Hope")
    type_text(driver, "editUserEmail", COLLECTOR_EMAIL)
    type_text(driver, "editUserPhone", "01611223399")
    choose_option(driver, "editUserArea", "Mirpur")
    type_text(driver, "editUserAddress", "Section 2")
    choose_option(driver, "editUserRole", "collector")
    type_text(driver, "editUserPassword", "Second#2026")
    click(driver, "saveUserBtn")
    message = wait_for_message(driver, "userModalMessage")
    return "already registered" in message, message


TEST_CASE = ("TC121", "Verify admin cannot add a user with an email that is already used",
             "Email: collector@foodbridge.com", test)


def run():
    return run_test_module("Admin", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
