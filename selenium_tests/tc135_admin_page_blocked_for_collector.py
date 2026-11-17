from helpers import *


def test(driver):
    login(driver, COLLECTOR_EMAIL, COLLECTOR_PASSWORD)
    open_page(driver, "admin-dashboard.html")
    sent_back = wait_for_url(driver, "collector-dashboard.html")
    return sent_back, "Collector was sent to: " + driver.current_url


TEST_CASE = ("TC135", "Verify a collector cannot open the admin dashboard",
             "Login: collector@foodbridge.com, open admin-dashboard.html", test)


def run():
    return run_test_module("Admin", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
