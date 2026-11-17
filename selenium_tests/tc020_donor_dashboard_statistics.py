from helpers import *


def test(driver):
    open_donor_dashboard(driver)
    rows = driver.find_elements(By.CSS_SELECTOR, "#foodTableBody tr[id^='food-']")
    waiting_items = driver.find_elements(By.CSS_SELECTOR, "#confirmList .confirm-item")
    total_stat = find(driver, "statTotal").text
    waiting_stat = find(driver, "statClaimed").text
    passed = total_stat == str(len(rows)) and waiting_stat == str(len(waiting_items))
    actual = (f"Total posts card = {total_stat}, rows in table = {len(rows)}; "
              f"Pickups to confirm card = {waiting_stat}, items in confirmation panel = {len(waiting_items)}")
    return passed, actual


TEST_CASE = ("TC20", "Verify dashboard statistics match the food list",
             "Compare Total posts and Pickups to confirm cards with the page", test)


def run():
    return run_test_module("Donor Dashboard", [TEST_CASE], login_as=(DONOR_EMAIL, DONOR_PASSWORD))


if __name__ == "__main__":
    run()
