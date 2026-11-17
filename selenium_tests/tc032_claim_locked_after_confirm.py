from helpers import *


def test(driver):
    login(driver, COLLECTOR_EMAIL, COLLECTOR_PASSWORD)
    wait_until_page_ready(driver, "claimsTableBody")
    wait_until(driver, lambda d: element_exists(d, "claim-row-2"))
    row_text = find(driver, "claim-row-2").text
    no_release_button = not element_exists(driver, "release-2")
    locked = element_exists(driver, "locked-2")
    passed = "Confirmed by donor" in row_text and no_release_button and locked
    return passed, f"Egg Fried Rice: 'Confirmed by donor', Release button shown: {not no_release_button}, Locked: {locked}"


TEST_CASE = ("TC32", "Verify collector cannot release food after donor confirmed pickup",
             "Login: collector@foodbridge.com, Egg Fried Rice (confirmed by donor)", test)


def run():
    return run_test_module("Pickup Confirmation & Home Page", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
