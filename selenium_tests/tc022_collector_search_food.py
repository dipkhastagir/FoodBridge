from helpers import *


def test(driver):
    open_collector_dashboard(driver)
    type_text(driver, "searchInput", "biryani")
    click(driver, "searchBtn")
    wait_until(driver, lambda d: len(visible_food_titles(d)) == 1)
    titles = visible_food_titles(driver)
    passed = len(titles) > 0 and all("biryani" in t.lower() for t in titles)
    return passed, f"Results: {titles}"


TEST_CASE = ("TC22", "Verify search food by keyword",
             "Search: biryani", test)


def run():
    return run_test_module("Collector Dashboard", [TEST_CASE], login_as=(COLLECTOR_EMAIL, COLLECTOR_PASSWORD))


if __name__ == "__main__":
    run()
