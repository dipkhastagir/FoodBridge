from helpers import *


def test(driver):
    login(driver, DONOR_EMAIL, DONOR_PASSWORD)
    wait_until_page_ready(driver, "confirmPanel")
    location = find(driver, "confirm-item-1").find_element(By.CSS_SELECTOR, ".collector-location").text
    passed = "Mirpur" in location and "Section 10, Block C" in location and "Open in Maps" in location
    return passed, "Collector location shown: " + location


TEST_CASE = ("TC47", "Verify donor sees the collector's location",
             "Login: donor@foodbridge.com, Vegetable Khichuri claimed by Hope Volunteers (Mirpur)", test)


def run():
    return run_test_module("Contact & Location", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
