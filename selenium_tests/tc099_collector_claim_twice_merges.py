from helpers import *


def test(driver):
    open_collector_dashboard(driver)
    type_text(driver, "claim-qty-1", "3")
    click(driver, "claim-1")
    wait_for_message(driver)
    type_text(driver, "claim-qty-1", "2")
    click(driver, "claim-1")
    wait_until(driver, lambda d: d.find_element(By.ID, "remaining-1").text == "15")
    rows = [r for r in driver.find_elements(By.CSS_SELECTOR, "#claimsTableBody tr") if "Chicken Biryani" in r.text]
    amount = rows[0].find_element(By.CSS_SELECTOR, ".claim-qty-cell").text if rows else "0"
    return len(rows) == 1 and amount == "5", "Chicken Biryani rows in My claims: " + str(len(rows)) + " | Servings: " + amount


TEST_CASE = ("TC99", "Verify claiming the same food twice adds to one claim",
             "Food: Chicken Biryani, Claim 3, then claim 2", test)


def run():
    return run_test_module("Collector Dashboard", [TEST_CASE], login_as=(COLLECTOR_EMAIL, COLLECTOR_PASSWORD))


if __name__ == "__main__":
    run()
