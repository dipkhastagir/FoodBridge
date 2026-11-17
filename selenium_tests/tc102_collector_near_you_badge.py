from helpers import *


def test(driver):
    login(driver, DONOR_EMAIL, DONOR_PASSWORD)
    open_donor_dashboard(driver)
    choose_option(driver, "foodArea", "Mirpur")
    fill_food_form(driver, "Mirpur Pitha", "Bakery", "12", "6", "Section 10", "")
    wait_for_message(driver)
    logout(driver)
    login(driver, COLLECTOR_EMAIL, COLLECTOR_PASSWORD)
    open_collector_dashboard(driver)
    card = find(driver, "food-card-6").text
    others = find(driver, "food-card-1").text
    passed = "Near you" in card and "Near you" not in others
    return passed, "Mirpur Pitha has Near you: " + str("Near you" in card) + " | Chicken Biryani (Banani) has it: " + str("Near you" in others)


TEST_CASE = ("TC102", "Verify food in the collector's own area shows a Near you badge",
             "Donor posts Mirpur Pitha in Mirpur, collector Hope Volunteers lives in Mirpur", test)


def run():
    return run_test_module("Collector Dashboard", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
