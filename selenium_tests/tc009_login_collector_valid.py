from helpers import *


def test(driver):
    fill_login_form(driver, COLLECTOR_EMAIL, COLLECTOR_PASSWORD)
    ok = wait_for_url(driver, "collector-dashboard.html")
    return ok, "Redirected to: " + driver.current_url


TEST_CASE = ("TC09", "Verify Collector login with valid credentials",
             "Email: collector@foodbridge.com, Password: collector123", test)


def run():
    return run_test_module("Login", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
