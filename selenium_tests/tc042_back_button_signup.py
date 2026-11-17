from helpers import *


def test(driver):
    open_page(driver, "signup.html")
    click(driver, "backBtn")
    on_home = wait_for_url(driver, "index.html")
    return on_home, "Back from sign up page went to: " + driver.current_url


TEST_CASE = ("TC42", "Verify Back button on sign up page goes to home page",
             "Open signup.html, click Back to Home", test)


def run():
    return run_test_module("Navigation", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
