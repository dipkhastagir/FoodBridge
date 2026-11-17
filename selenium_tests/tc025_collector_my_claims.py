from helpers import *


def test(driver):
    open_collector_dashboard(driver)
    type_text(driver, "claim-qty-1", "5")
    click(driver, "claim-1")
    wait_for_message(driver)
    claims_text = find(driver, "claimsTableBody").text
    passed = "Vegetable Khichuri" in claims_text and "Chicken Biryani" in claims_text
    rows = driver.find_elements(By.CSS_SELECTOR, "#claimsTableBody tr[id^='claim-row-']")
    return passed, f"My claims table has {len(rows)} rows (Vegetable Khichuri, Chicken Biryani found: {passed})"


TEST_CASE = ("TC25", "Verify claimed food appears in My claims",
             "Claim 5 Chicken Biryani first, then check My claims (expected: Vegetable Khichuri, Chicken Biryani)", test)


def run():
    return run_test_module("Collector Dashboard", [TEST_CASE], login_as=(COLLECTOR_EMAIL, COLLECTOR_PASSWORD))


if __name__ == "__main__":
    run()
