from helpers import *


def test(driver):
    fill_login_form(driver, DONOR_EMAIL, DONOR_PASSWORD)
    ok = wait_for_url(driver, "donor-dashboard.html")
    return ok, "Redirected to: " + driver.current_url


TEST_CASE = ("TC08", "Verify Donor login with valid credentials",
             "Email: donor@foodbridge.com, Password: donor123", test)


def run():
    return run_test_module("Login", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
