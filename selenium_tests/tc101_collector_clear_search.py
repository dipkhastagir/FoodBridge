from helpers import *


def test(driver):
    open_collector_dashboard(driver)
    type_text(driver, "searchInput", "biryani")
    click(driver, "searchBtn")
    wait_until(driver, lambda d: len(visible_food_titles(d)) == 1)
    click(driver, "clearSearchBtn")
    wait_until(driver, lambda d: len(visible_food_titles(d)) == 3)
    box = find(driver, "searchInput").get_attribute("value")
    return box == "" and len(visible_food_titles(driver)) == 3, "Food shown after Clear: " + str(len(visible_food_titles(driver)))


TEST_CASE = ("TC101", "Verify the Clear button removes the search and shows all food again",
             "Search: biryani, then click Clear", test)


def run():
    return run_test_module("Collector Dashboard", [TEST_CASE], login_as=(COLLECTOR_EMAIL, COLLECTOR_PASSWORD))


if __name__ == "__main__":
    run()
