from helpers import *


def test(driver):
    open_page(driver, "login.html")
    email = find(driver, "email")
    password = find(driver, "password")
    empty = email.get_attribute("value") == "" and password.get_attribute("value") == ""
    locked = email.get_attribute("readonly") is not None and password.get_attribute("readonly") is not None
    return empty and locked, "Boxes empty: " + str(empty) + " | Locked until clicked: " + str(locked)


TEST_CASE = ("TC74", "Verify the login boxes are empty and locked against autofill when the page opens",
             "Open login.html", test)


def run():
    return run_test_module("Login", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
