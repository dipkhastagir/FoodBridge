from helpers import *


def test(driver):
    login(driver, DONOR_EMAIL, DONOR_PASSWORD)
    wait_until_page_ready(driver, "switchRoleBtn")
    click(driver, "switchRoleBtn")
    accept_alert(driver)
    wait_for_url(driver, "collector-dashboard.html")
    logout(driver)
    login(driver, DONOR_EMAIL, DONOR_PASSWORD)
    kept = wait_for_url(driver, "collector-dashboard.html")
    return kept, "After logging in again: " + driver.current_url


TEST_CASE = ("TC106", "Verify a switched role is kept after logging out and in again",
             "Donor switches to Collector, logs out, logs in again", test)


def run():
    return run_test_module("Role Switch", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
