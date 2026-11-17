from helpers import *


def test(driver):
    login(driver, COLLECTOR_EMAIL, COLLECTOR_PASSWORD)
    wait_until_page_ready(driver, "searchBtn")
    type_text(driver, "claim-qty-2", "5")
    click(driver, "claim-2")
    wait_for_message(driver)
    could_release_before = element_exists(driver, "release-3")

    logout(driver)
    login(driver, DONOR_EMAIL, DONOR_PASSWORD)
    wait_until_page_ready(driver, "confirmPanel")
    click(driver, "confirm-3")
    donor_message = wait_for_message(driver)

    logout(driver)
    login(driver, COLLECTOR_EMAIL, COLLECTOR_PASSWORD)
    wait_until_page_ready(driver, "claimsTableBody")
    wait_until(driver, lambda d: element_exists(d, "claim-row-3"))
    can_release_after = element_exists(driver, "release-3")
    locked_after = element_exists(driver, "locked-3")

    passed = could_release_before and "Pickup confirmed" in donor_message and not can_release_after and locked_after
    actual = (f"Release button before confirmation: {could_release_before} | Donor: {donor_message} | "
              f"Release button after confirmation: {can_release_after}, Locked: {locked_after}")
    return passed, actual


TEST_CASE = ("TC33", "Verify full claim, confirm and lock flow",
             "Collector claims 5 Fresh Bread Loaves, Donor confirms, Collector checks My claims", test)


def run():
    return run_test_module("Pickup Confirmation & Home Page", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
