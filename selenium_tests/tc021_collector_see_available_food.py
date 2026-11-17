from helpers import *


def test(driver):
    open_collector_dashboard(driver)
    titles = visible_food_titles(driver)
    claimed_hidden = "Vegetable Khichuri" not in titles
    passed = len(titles) > 0 and claimed_hidden
    return passed, f"{len(titles)} food tickets shown: {titles}"


TEST_CASE = ("TC21", "Verify collector can see available food",
             "Open Collector Dashboard", test)


def run():
    return run_test_module("Collector Dashboard", [TEST_CASE], login_as=(COLLECTOR_EMAIL, COLLECTOR_PASSWORD))


if __name__ == "__main__":
    run()
