from helpers import *


def test(driver):
    open_page(driver, "signup.html")
    type_text(driver, "phone", "01a7-11 22+33 44")
    value = find(driver, "phone").get_attribute("value")
    return value == "01711223344", "Mobile box shows: " + value


TEST_CASE = ("TC67", "Verify letters, spaces and symbols are removed from the mobile box",
             "Mobile typed: 01a7-11 22+33 44", test)


def run():
    return run_test_module("Sign Up", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
