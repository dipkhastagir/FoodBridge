from helpers import *


def test(driver):
    open_collector_dashboard(driver)
    type_text(driver, "searchInput", "pizza")
    click(driver, "searchBtn")
    wait_until(driver, lambda d: d.find_element(By.ID, "emptyState").is_displayed())
    text = find(driver, "emptyState").text
    return "No food matches" in text and len(visible_food_titles(driver)) == 0, text


TEST_CASE = ("TC103", "Verify a search with no match shows the empty message",
             "Search: pizza", test)


def run():
    return run_test_module("Collector Dashboard", [TEST_CASE], login_as=(COLLECTOR_EMAIL, COLLECTOR_PASSWORD))


if __name__ == "__main__":
    run()
