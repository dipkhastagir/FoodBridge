from helpers import *


def test(driver):
    login(driver, ADMIN_EMAIL, ADMIN_PASSWORD)
    on_admin = wait_for_url(driver, "admin-dashboard.html")
    wait_until_page_ready(driver, "statDonors")
    wait_until(driver, lambda d: d.find_element(By.ID, "statCollectors").text != "0")
    donors = find(driver, "statDonors").text
    collectors = find(driver, "statCollectors").text
    passed = on_admin and donors == "1" and collectors == "2"
    return passed, f"Opened: {driver.current_url} | Donors: {donors}, Collectors: {collectors}"


TEST_CASE = ("TC48", "Verify admin login opens the admin dashboard",
             "Email: admin@foodbridge.com, Password: Admin@FoodBridge26", test)


def run():
    return run_test_module("Admin", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
