from helpers import *


def test(driver):
    login(driver, DONOR_EMAIL, DONOR_PASSWORD)
    wait_until_page_ready(driver, "logoutBtn")
    click(driver, "logoutBtn")
    went_to_login = wait_for_url(driver, "login.html")

    open_page(driver, "donor-dashboard.html")
    blocked = wait_for_url(driver, "login.html")
    return went_to_login and blocked, "After logout, dashboard opened: " + driver.current_url


TEST_CASE = ("TC29", "Verify logout and dashboard access after logout",
             "Click Log out, then open donor-dashboard.html", test)


def run():
    return run_test_module("Profile & Security", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
