from helpers import *


def test(driver):
    open_admin_tab(driver, "tab-users", "usersBody")
    click(driver, "delete-user-3")
    accept_alert(driver)
    message = wait_for_message(driver)
    wait_until(driver, lambda d: not element_exists(d, "user-3"))
    removed = not element_exists(driver, "user-3")

    logout(driver)
    open_page(driver, "login.html")
    type_text(driver, "email", COLLECTOR2_EMAIL)
    type_text(driver, "password", COLLECTOR2_PASSWORD)
    click(driver, "loginBtn")
    login_message = wait_for_message(driver)

    passed = "was deleted" in message and removed and login_message == "Invalid email or password."
    return passed, message + " | Removed from list: " + str(removed) + " | Login attempt: " + login_message


TEST_CASE = ("TC60", "Verify admin can delete a user",
             "User: Smile Foundation (smile@foodbridge.com), click Delete, click OK, then try to log in", test)


def run():
    return run_test_module("Admin", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
