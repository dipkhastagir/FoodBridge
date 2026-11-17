from helpers import *


def test(driver):
    open_page(driver, "reset-password.html")
    click(driver, "backBtn")
    on_forgot = wait_for_url(driver, "forgot-password.html")
    return on_forgot, "Went to: " + driver.current_url


TEST_CASE = ("TC139", "Verify the Back button on the code page goes to the forgot password page",
             "Open reset-password.html, click Back to Forgot password", test)


def run():
    return run_test_module("Navigation", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
