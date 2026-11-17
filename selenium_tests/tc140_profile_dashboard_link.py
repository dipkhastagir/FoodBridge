from helpers import *


def test(driver):
    login(driver, DONOR_EMAIL, DONOR_PASSWORD)
    open_profile(driver)
    wait_until(driver, lambda d: "dashboard" in d.find_element(By.ID, "navDashboard").get_attribute("href"))
    click(driver, "navDashboard")
    on_dashboard = wait_for_url(driver, "donor-dashboard.html")
    return on_dashboard, "Went to: " + driver.current_url


TEST_CASE = ("TC140", "Verify the Dashboard link on the profile page opens the user's own dashboard",
             "Login: donor@foodbridge.com, open Profile, click Dashboard", test)


def run():
    return run_test_module("Navigation", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
