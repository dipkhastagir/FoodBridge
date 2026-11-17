from helpers import *


def test(driver):
    open_page(driver, "signup.html")
    type_text(driver, "phone", "017112233445")
    value = find(driver, "phone").get_attribute("value")
    return value == "01711223344", "Mobile box shows: " + value + " (" + str(len(value)) + " digits)"


TEST_CASE = ("TC63", "Verify mobile box keeps only 11 digits when 12 are typed",
             "Mobile typed: 017112233445 (12 digits)", test)


def run():
    return run_test_module("Sign Up", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
