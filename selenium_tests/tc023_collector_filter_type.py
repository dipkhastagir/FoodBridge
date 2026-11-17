from helpers import *


def test(driver):
    open_collector_dashboard(driver)
    choose_option(driver, "typeFilter", "Bakery")
    click(driver, "searchBtn")
    wait_until(
        driver, lambda d: all(t.text == "Bakery" for t in d.find_elements(By.CSS_SELECTOR, "#foodGrid .food-type"))
    )
    types = [t.text for t in driver.find_elements(By.CSS_SELECTOR, "#foodGrid .food-type")]
    passed = len(types) > 0 and all(t == "Bakery" for t in types)
    return passed, f"Food types shown: {types}"


TEST_CASE = ("TC23", "Verify filter food by type",
             "Food type: Bakery", test)


def run():
    return run_test_module("Collector Dashboard", [TEST_CASE], login_as=(COLLECTOR_EMAIL, COLLECTOR_PASSWORD))


if __name__ == "__main__":
    run()
