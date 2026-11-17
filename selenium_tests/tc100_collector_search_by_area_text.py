from helpers import *


def test(driver):
    open_collector_dashboard(driver)
    type_text(driver, "searchInput", "gulshan")
    click(driver, "searchBtn")
    wait_until(driver, lambda d: len(visible_food_titles(d)) == 1)
    titles = visible_food_titles(driver)
    return titles == ["Fresh Bread Loaves"], "Results: " + str(titles)


TEST_CASE = ("TC100", "Verify the search box also finds food by area name",
             "Search: gulshan", test)


def run():
    return run_test_module("Collector Dashboard", [TEST_CASE], login_as=(COLLECTOR_EMAIL, COLLECTOR_PASSWORD))


if __name__ == "__main__":
    run()
