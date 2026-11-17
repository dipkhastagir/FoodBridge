from helpers import *


def test(driver):
    login(driver, DONOR_EMAIL, DONOR_PASSWORD)
    wait_until_page_ready(driver, "confirmPanel")
    item_text = find(driver, "confirm-item-1").text
    count = find(driver, "confirmCount").text
    passed = "Vegetable Khichuri" in item_text and "Hope Volunteers" in item_text and count == "1"
    actual = (f"Panel count = {count}; Vegetable Khichuri shown: {'Vegetable Khichuri' in item_text}; "
              f"Claimed by Hope Volunteers shown: {'Hope Volunteers' in item_text}")
    return passed, actual


TEST_CASE = ("TC31", "Verify donor sees claimed food in the confirmation panel",
             "Login: donor@foodbridge.com, Vegetable Khichuri claimed by Hope Volunteers", test)


def run():
    return run_test_module("Pickup Confirmation & Home Page", [TEST_CASE], logout_before_each=True)


if __name__ == "__main__":
    run()
