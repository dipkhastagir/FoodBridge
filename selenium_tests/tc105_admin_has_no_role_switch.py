from helpers import *


def test(driver):
    open_admin_dashboard(driver)
    no_button = not element_exists(driver, "switchRoleBtn")
    return no_button, "Switch role button on admin page: " + str(not no_button)


TEST_CASE = ("TC105", "Verify the admin dashboard has no role switch button",
             "Login: admin@foodbridge.com", test)


def run():
    return run_test_module("Role Switch", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
