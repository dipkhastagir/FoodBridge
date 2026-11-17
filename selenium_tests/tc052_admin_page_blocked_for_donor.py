from helpers import *


def test(driver):
    login(driver, DONOR_EMAIL, DONOR_PASSWORD)
    open_page(driver, "admin-dashboard.html")
    sent_back = wait_for_url(driver, "donor-dashboard.html")
    return sent_back, "Donor was sent to: " + driver.current_url


TEST_CASE = ("TC52", "Verify a donor cannot open the admin dashboard",
             "Login: donor@foodbridge.com, open admin-dashboard.html", test)


def run():
    return run_test_module("Admin", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
