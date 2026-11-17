from helpers import *


def test(driver):
    open_page(driver, "login.html")
    click(driver, "backBtn")
    on_home = wait_for_url(driver, "index.html")
    return on_home, "Went to: " + driver.current_url


TEST_CASE = ("TC138", "Verify the Back button on the login page goes to the home page",
             "Open login.html, click Back to Home", test)


def run():
    return run_test_module("Navigation", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
