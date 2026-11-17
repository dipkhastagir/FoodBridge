from helpers import *


def test(driver):
    login(driver, COLLECTOR_EMAIL, COLLECTOR_PASSWORD)
    open_page(driver, "donor-dashboard.html")
    redirected = wait_for_url(driver, "collector-dashboard.html")
    return redirected, "Collector was sent to: " + driver.current_url


TEST_CASE = ("TC30", "Verify a Collector cannot open the Donor dashboard",
             "Login: collector@foodbridge.com, open donor-dashboard.html", test)


def run():
    return run_test_module("Profile & Security", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
