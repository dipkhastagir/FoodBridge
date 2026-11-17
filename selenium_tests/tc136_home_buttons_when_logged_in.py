from helpers import *


def test(driver):
    login(driver, DONOR_EMAIL, DONOR_PASSWORD)
    open_page(driver, "index.html")
    wait_until(driver, lambda d: d.find_element(By.ID, "navSignupBtn").text == "Go to dashboard")
    names = [find(driver, "navLoginBtn").text, find(driver, "navSignupBtn").text]
    return names == ["Log out", "Go to dashboard"], "Buttons: " + str(names)


TEST_CASE = ("TC136", "Verify the home page buttons change when the user is logged in",
             "Login: donor@foodbridge.com, open index.html", test)


def run():
    return run_test_module("Home Page", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
