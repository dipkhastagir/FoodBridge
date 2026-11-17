from helpers import *


def test(driver):
    login(driver, COLLECTOR_EMAIL, COLLECTOR_PASSWORD)
    wait_until_page_ready(driver, "searchBtn")
    wait_until(driver, lambda d: len(d.find_elements(By.CSS_SELECTOR, "#areaFilter option")) > 1)
    choose_option(driver, "areaFilter", "Gulshan")
    click(driver, "searchBtn")
    wait_until(driver, lambda d: len(d.find_elements(By.CSS_SELECTOR, "#foodGrid .food-card")) == 1)
    areas = [a.text for a in driver.find_elements(By.CSS_SELECTOR, "#foodGrid .food-area strong")]
    has_map = len(driver.find_elements(By.CSS_SELECTOR, "#foodGrid .map-link")) == 1
    passed = areas == ["Gulshan"] and has_map
    return passed, f"Areas shown: {areas} | Open in Maps link: {has_map}"


TEST_CASE = ("TC46", "Verify collector can find food by area",
             "Login: collector@foodbridge.com, Area: Gulshan, click Search", test)


def run():
    return run_test_module("Contact & Location", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
