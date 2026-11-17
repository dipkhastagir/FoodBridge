from helpers import *


def test(driver):
    fill_login_form(driver, "DONOR@FOODBRIDGE.COM", DONOR_PASSWORD)
    ok = wait_for_url(driver, "donor-dashboard.html")
    return ok, "Opened: " + driver.current_url


TEST_CASE = ("TC73", "Verify login works with the email typed in capital letters",
             "Email: DONOR@FOODBRIDGE.COM, Password: Donor@FoodBridge26", test)


def run():
    return run_test_module("Login", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
