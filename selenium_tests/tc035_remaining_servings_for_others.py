from helpers import *


def test(driver):
    login(driver, COLLECTOR_EMAIL, COLLECTOR_PASSWORD)
    open_collector_dashboard(driver)
    type_text(driver, "claim-qty-2", "8")
    click(driver, "claim-2")
    first_message = wait_for_message(driver)
    left_after_first = find(driver, "remaining-2").text

    logout(driver)
    login(driver, COLLECTOR2_EMAIL, COLLECTOR2_PASSWORD)
    open_collector_dashboard(driver)
    left_seen_by_second = find(driver, "remaining-2").text
    type_text(driver, "claim-qty-2", "7")
    click(driver, "claim-2")
    second_message = wait_for_message(driver)
    gone = not element_exists(driver, "food-card-2")

    passed = (left_after_first == "7" and left_seen_by_second == "7"
              and "last of it" in second_message and gone)
    actual = (f"After 8 claimed: {left_after_first} left | Second collector saw: {left_seen_by_second} left | "
              f"{second_message} | Removed from list: {gone}")
    return passed, actual


TEST_CASE = ("TC35", "Verify remaining servings stay available for other collectors",
             "Collector 1 claims 8 of 15 Fresh Bread Loaves, Collector 2 (smile@foodbridge.com) claims the last 7", test)


def run():
    return run_test_module("Partial Claim", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
