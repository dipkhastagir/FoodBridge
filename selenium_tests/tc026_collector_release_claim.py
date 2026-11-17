from helpers import *


def test(driver):
    open_collector_dashboard(driver)
    type_text(driver, "claim-qty-1", "5")
    click(driver, "claim-1")
    wait_for_message(driver)
    click(driver, "release-3")
    accept_alert(driver)
    message = wait_for_message(driver)
    left = find(driver, "remaining-1").text
    return "released" in message.lower() and left == "20", message + " | Servings left on the ticket: " + left


TEST_CASE = ("TC26", "Verify collector can release a claim before pickup",
             "Claim 5 Chicken Biryani, then Release it and click OK on the confirm box", test)


def run():
    return run_test_module("Collector Dashboard", [TEST_CASE], login_as=(COLLECTOR_EMAIL, COLLECTOR_PASSWORD))


if __name__ == "__main__":
    run()
