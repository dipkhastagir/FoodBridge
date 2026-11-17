from helpers import *


def test(driver):
    open_page(driver, "forgot-password.html")
    click(driver, "backBtn")
    on_login = wait_for_url(driver, "login.html")
    return on_login, "Back from forgot password page went to: " + driver.current_url


TEST_CASE = ("TC43", "Verify Back button on forgot password page goes to log in page",
             "Open forgot-password.html, click Back to Log in", test)


def run():
    return run_test_module("Navigation", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
