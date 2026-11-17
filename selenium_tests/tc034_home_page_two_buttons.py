from helpers import *


def test(driver):
    open_page(driver, "index.html")
    wait_until(driver, lambda d: "waiting" in d.find_element(By.ID, "liveText").text)
    buttons = driver.find_elements(By.CSS_SELECTOR, ".btn")
    names = [b.text for b in buttons]
    live = find(driver, "liveText").text
    passed = names == ["Log in", "Create account"] and "waiting for a collector" in live
    return passed, f"Buttons: {names} | Live text: {live}"


TEST_CASE = ("TC34", "Verify home page shows only Log in and Create account buttons",
             "Open http://localhost:3000", test)


def run():
    return run_test_module("Pickup Confirmation & Home Page", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
